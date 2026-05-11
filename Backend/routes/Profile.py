from fastapi import APIRouter

router=APIRouter(tags=["profile"])

@router.get("/")
async def profile_details():
    return {
        "name":"Jeeva",
        "age":24
    }
