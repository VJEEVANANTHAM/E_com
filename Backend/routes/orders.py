from datetime import datetime, timedelta
import hmac
import hashlib
import os

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import requests

from database import get_db
from models.Cart import CartItem
from models.Order import Order
from models.Products import Product
from models.Signup import User
from routes.cart import get_current_user


router = APIRouter(prefix="/orders", tags=["Orders"])


class PaymentRequest(BaseModel):
    amount: float = Field(gt=0)


class ShippingAddress(BaseModel):
    street: str
    city: str
    state: str
    pincode: str


class VerifyPaymentRequest(BaseModel):
    razorpay_order_id: str
    razorpay_payment_id: str
    razorpay_signature: str
    shippingAddress: ShippingAddress


class DummyPaymentRequest(BaseModel):
    shippingAddress: ShippingAddress


def serialize_order(order: Order, user: User | None = None):
    data = {
        "_id": str(order.id),
        "items": order.items,
        "shippingAddress": order.shipping_address,
        "totalAmount": float(order.total_amount),
        "status": order.status,
        "isPaid": order.is_paid,
        "createdAt": order.created_at.isoformat() if order.created_at else None,
        "expectedDelivery": order.expected_delivery.isoformat() if order.expected_delivery else None,
    }

    if user:
        data["user"] = {
            "_id": str(user.id),
            "username": user.full_name,
            "email": user.email,
        }

    return data


def get_cart_snapshot(db: Session, user_id: int):
    rows = (
        db.query(CartItem, Product)
        .join(Product, Product.id == CartItem.product_id)
        .filter(CartItem.user_id == user_id)
        .all()
    )

    items = []

    for cart_item, product in rows:
        items.append({
            "productId": product.mongo_id or str(product.id),
            "name": product.name,
            "price": float(product.price or 0),
            "quantity": cart_item.quantity,
            "image": product.image,
        })

    return items


def place_order_from_cart(
    db: Session,
    user: User,
    shipping_address: ShippingAddress,
    razorpay_order_id: str | None = None,
    razorpay_payment_id: str | None = None,
    razorpay_signature: str | None = None,
):
    cart_items = get_cart_snapshot(db, user.id)

    if not cart_items:
        raise HTTPException(status_code=400, detail="Your cart is empty")

    total = sum(item["price"] * item["quantity"] for item in cart_items)

    order = Order(
        user_id=user.id,
        items=cart_items,
        shipping_address=shipping_address.model_dump(),
        total_amount=total,
        status="placed",
        is_paid=True,
        razorpay_order_id=razorpay_order_id,
        razorpay_payment_id=razorpay_payment_id,
        razorpay_signature=razorpay_signature,
        expected_delivery=datetime.utcnow() + timedelta(days=5),
    )

    db.add(order)
    db.query(CartItem).filter(CartItem.user_id == user.id).delete()
    db.commit()
    db.refresh(order)

    return order


def verify_razorpay_signature(data: VerifyPaymentRequest):
    key_secret = os.getenv("RAZORPAY_KEY_SECRET")

    if not key_secret:
        return

    message = f"{data.razorpay_order_id}|{data.razorpay_payment_id}".encode()
    expected_signature = hmac.new(
        key_secret.encode(),
        message,
        hashlib.sha256,
    ).hexdigest()

    if not hmac.compare_digest(expected_signature, data.razorpay_signature):
        raise HTTPException(status_code=400, detail="Invalid payment signature")


@router.get("/")
def get_orders(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    orders = (
        db.query(Order)
        .filter(Order.user_id == user.id)
        .order_by(Order.created_at.desc())
        .all()
    )

    return [serialize_order(order) for order in orders]


@router.post("/create-payment")
def create_payment(
    data: PaymentRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cart_items = get_cart_snapshot(db, user.id)

    if not cart_items:
        raise HTTPException(status_code=400, detail="Your cart is empty")

    total = sum(item["price"] * item["quantity"] for item in cart_items)
    amount_paise = int(total * 100)
    key_id = os.getenv("RAZORPAY_KEY_ID")
    key_secret = os.getenv("RAZORPAY_KEY_SECRET")

    if key_id and key_secret:
        response = requests.post(
            "https://api.razorpay.com/v1/orders",
            auth=(key_id, key_secret),
            json={
                "amount": amount_paise,
                "currency": "INR",
                "receipt": f"user_{user.id}_{int(datetime.utcnow().timestamp())}",
            },
            timeout=15,
        )

        if response.status_code >= 400:
            raise HTTPException(status_code=502, detail="Unable to create payment order")

        razorpay_order = response.json()

        return {
            "orderId": razorpay_order["id"],
            "amount": razorpay_order["amount"],
            "currency": razorpay_order["currency"],
        }

    return {
        "orderId": f"order_{user.id}_{int(datetime.utcnow().timestamp())}",
        "amount": amount_paise,
        "currency": "INR",
    }


@router.post("/verify-payment")
def verify_payment(
    data: VerifyPaymentRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    cart_items = get_cart_snapshot(db, user.id)

    if not cart_items:
        raise HTTPException(status_code=400, detail="Your cart is empty")

    verify_razorpay_signature(data)

    order = place_order_from_cart(
        db=db,
        user=user,
        shipping_address=data.shippingAddress,
        razorpay_order_id=data.razorpay_order_id,
        razorpay_payment_id=data.razorpay_payment_id,
        razorpay_signature=data.razorpay_signature,
    )

    return {
        "message": "Order placed successfully",
        "order": serialize_order(order),
    }


@router.post("/dummy-payment")
def dummy_payment(
    data: DummyPaymentRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order = place_order_from_cart(
        db=db,
        user=user,
        shipping_address=data.shippingAddress,
        razorpay_order_id=f"dummy_order_{user.id}_{int(datetime.utcnow().timestamp())}",
        razorpay_payment_id=f"dummy_payment_{user.id}_{int(datetime.utcnow().timestamp())}",
        razorpay_signature="dummy_signature",
    )

    return {
        "message": "Payment done",
        "order": serialize_order(order),
    }


@router.put("/{order_id}/cancel")
def cancel_order(
    order_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = "cancelled"
    db.commit()

    return {
        "message": "Order cancelled",
        "refundAmount": float(order.total_amount),
    }


@router.put("/{order_id}/return")
def return_order(
    order_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    order = db.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = "returned"
    db.commit()

    return {
        "message": "Return submitted",
        "refundAmount": float(order.total_amount),
    }
