from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.Signup import Signup
from models.Signup import User
from schemas.Login import Login,Token
from dotenv import load_dotenv
from pwdlib import PasswordHash
import jwt
from jwt.exceptions import InvalidTokenError
import os
from datetime import datetime, timedelta, timezone

#hasing password

password_hash = PasswordHash.recommended()

DUMMY_HASH = password_hash.hash("dummypassword")


def get_password_hash(password):
    return password_hash.hash(password)


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


router = APIRouter()

User_Email=""

@router.post("/signup")
def signup(
    data: Signup,
    db: Session = Depends(get_db)
):
    hashed_password = get_password_hash(data.Password)

    new_user = User(
        full_name=data.full_name,
        email=data.Email_Address,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    

    return {
        "message": "User created successfully"
    }

load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")

ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/Login")
def login_validate(data: Login, db: Session = Depends(get_db)): 
    user = db.query(User).filter(User.email==data.email).first()

    # print(user.email)

    if not user:
        return "Check the email" 

    print(user.password,data.password)
 
    if not verify_password(data.password,user.password,):
        return "Password does not match"
    User_Email=user.email
    print("User_Email",User_Email)
    
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=timedelta(minutes=30)
    )
    
    return {
        "_id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "isAdmin": False,
        "balance": 0,
        "token": access_token,
        "access_token": access_token,
        "token_type": "bearer"
    }
# print(f"{}")
