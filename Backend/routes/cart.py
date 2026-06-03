from fastapi import APIRouter, Depends, Header, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import jwt
import os

from database import get_db
from models.Cart import CartItem
from models.Products import Product
from models.Signup import User
from routes.products import serialize_product


router = APIRouter(prefix="/cart", tags=["Cart"])


class CartRequest(BaseModel):
    productId: str
    quantity: int = Field(default=1, ge=1)


def get_current_user(
    authorization: str | None = Header(default=None),
    db: Session = Depends(get_db),
):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    token = authorization.split(" ", 1)[1]

    try:
        payload = jwt.decode(
            token,
            os.getenv("JWT_SECRET_KEY"),
            algorithms=[os.getenv("ALGORITHM")],
        )
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    email = payload.get("sub")
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    return user


def find_product(db: Session, product_id: str):
    product = None

    if product_id.isdigit():
        product = db.query(Product).filter(Product.id == int(product_id)).first()

    if not product:
        product = db.query(Product).filter(Product.mongo_id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


def serialize_cart(db: Session, user_id: int):
    items = (
        db.query(CartItem, Product)
        .join(Product, Product.id == CartItem.product_id)
        .filter(CartItem.user_id == user_id)
        .all()
    )

    return {
        "items": [
            {
                "product": serialize_product(product),
                "quantity": cart_item.quantity,
            }
            for cart_item, product in items
        ]
    }


@router.get("/")
def get_cart(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return serialize_cart(db, user.id)


@router.post("/")
def add_to_cart(
    data: CartRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = find_product(db, data.productId)

    cart_item = (
        db.query(CartItem)
        .filter(CartItem.user_id == user.id, CartItem.product_id == product.id)
        .first()
    )

    if cart_item:
        cart_item.quantity += data.quantity
    else:
        cart_item = CartItem(user_id=user.id, product_id=product.id, quantity=data.quantity)
        db.add(cart_item)

    db.commit()

    return {
        "message": "Product added to cart",
        "cart": serialize_cart(db, user.id),
    }


@router.put("/")
def update_cart_item(
    data: CartRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = find_product(db, data.productId)
    cart_item = (
        db.query(CartItem)
        .filter(CartItem.user_id == user.id, CartItem.product_id == product.id)
        .first()
    )

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    cart_item.quantity = data.quantity
    db.commit()

    return {
        "message": "Cart updated",
        "cart": serialize_cart(db, user.id),
    }


@router.delete("/clear")
def clear_cart(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    db.query(CartItem).filter(CartItem.user_id == user.id).delete()
    db.commit()

    return {
        "message": "Cart cleared",
        "cart": {"items": []},
    }


@router.delete("/{product_id}")
def remove_from_cart(
    product_id: str,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    product = find_product(db, product_id)
    cart_item = (
        db.query(CartItem)
        .filter(CartItem.user_id == user.id, CartItem.product_id == product.id)
        .first()
    )

    if cart_item:
        db.delete(cart_item)
        db.commit()

    return {
        "message": "Product removed from cart",
        "cart": serialize_cart(db, user.id),
    }
