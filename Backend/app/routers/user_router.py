from fastapi import APIRouter, Depends
from app.middleware.auth_middleware import get_current_user

router = APIRouter()

@router.get("/me")
async def get_user(current_user = Depends(get_current_user)):
    return current_user