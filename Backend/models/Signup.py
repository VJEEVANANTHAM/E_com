

from sqlalchemy import Column,Integer,String
from database import Base

class User(Base):
    __tablename__="user_details"

    id=Column(Integer,primary_key=True,index=True)
    full_name=Column(String(30),nullable=False)
    email=Column(String(40),unique=True,index=True)
    password=Column(String(225),nullable=False)
