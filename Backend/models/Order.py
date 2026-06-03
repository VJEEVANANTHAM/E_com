from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, JSON, Numeric, String
from sqlalchemy.sql import func

from database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user_details.id"), nullable=False, index=True)
    items = Column(JSON, nullable=False)
    shipping_address = Column(JSON, nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(30), nullable=False, default="placed")
    is_paid = Column(Boolean, nullable=False, default=True)
    razorpay_order_id = Column(String(100), nullable=True)
    razorpay_payment_id = Column(String(100), nullable=True)
    razorpay_signature = Column(String(255), nullable=True)
    expected_delivery = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
