from fastapi import APIRouter,Depends
from database import get_db
from sqlalchemy.orm import Session
from schemas.Signup import Update_Profile,Update_password
from sqlalchemy import update
from models.Signup import User
router=APIRouter(tags=["profile"])

@router.put("/update_password")
def profile_details(
    data:Update_password,
    db:Session=Depends(get_db)
    ):
    # user = db.query(User).filter(User.email==data.email).first()
    # user.password=data.newPassword
    
    # db.commit()
    # db.refresh(user)
    # return "password successfully changed"
    pass

@router.put("/profile")
def Update_Personal_Information(
    data:Update_Profile,
    db:Session=Depends(get_db)
    ):
    
    user = None

    print(user.full_name)
    print(user.email)
  
    user.full_name = data.username
    user.email = data.email
    
    db.commit()
    db.refresh(user)

    if not user:
        return "Check the email"
    
    return "profile updated successfully"
            