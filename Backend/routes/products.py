from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models.Products import Product

router = APIRouter()


@router.get("/")
def get_products(
    db: Session = Depends(get_db)
):

    products = db.query(Product).all()

    return products