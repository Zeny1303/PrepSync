from fastapi import APIRouter
from app.schemas.user_schema import UserSignup, UserLogin
from app.controllers import auth_controller

router = APIRouter()


@router.post("/signup")
async def signup(user: UserSignup):
    return await auth_controller.signup(user)


@router.post("/login")
async def login(user: UserLogin):
    return await auth_controller.login(user)


@router.post("/logout")
async def logout():
    return await auth_controller.logout()