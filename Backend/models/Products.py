from sqlalchemy import (
    Column,
    Integer,
    String,
    DECIMAL,
    Text,
    DateTime
)

from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    mongo_id = Column(String(50), unique=True)
    name = Column(String(255), nullable=False)
    category = Column(String(100))
    price = Column(DECIMAL(10, 2))
    rating = Column(DECIMAL(2, 1))
    reviews = Column(Integer)
    image = Column(String(255))
    description = Column(Text)
    stock = Column(Integer)
    version = Column(Integer)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    

