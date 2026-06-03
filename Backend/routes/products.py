from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from models.Products import Product

router = APIRouter()


def serialize_product(product: Product):
    return {
        "_id": product.mongo_id or str(product.id),
        "id": product.id,
        "name": product.name,
        "category": product.category,
        "price": float(product.price or 0),
        "rating": float(product.rating or 0),
        "reviews": product.reviews or 0,
        "image": product.image,
        "description": product.description,
        "stock": product.stock or 0,
    }


@router.get("/")
def get_products(
    category: str | None = Query(default=None),
    db: Session = Depends(get_db)
):
    query = db.query(Product)

    if category:
        query = query.filter(Product.category == category)

    products = query.all()

    return [serialize_product(product) for product in products]


@router.get("/{product_id}")
def get_product(
    product_id: str,
    db: Session = Depends(get_db)
):  
    product = None

    if product_id.isdigit():
        product = db.query(Product).filter(Product.id == int(product_id)).first()

    if not product:
        product = db.query(Product).filter(Product.mongo_id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return serialize_product(product)
