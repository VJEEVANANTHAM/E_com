from fastapi import APIRouter

router=APIRouter()

@router.get("/")
def payment():
    return {"user name":"Jeeva","age":24}

