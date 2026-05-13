from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from passlib.context import CryptContext

from database import get_db
from schemas.Signup import Signup
from models.Signup import User

router = APIRouter()


@router.post("/")
def signup(
    data: Signup,
    db: Session = Depends(get_db)
):
    # check = db.query(User).filter_by(
    #     email=data.Email_Address
    # ).first()
    # print(check)
    # if check:

    #     return {
    #         "message": "The email already exists"
    #     }

    new_user = User(
        full_name=data.full_name,
        email=data.Email_Address,
        password=data.Password
        )
  
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created successfully"
    }
    