from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt
import os
from app.database import users_collection
from dotenv import load_dotenv

load_dotenv()

security = HTTPBearer()

JWT_SECRET = os.getenv("JWT_SECRET")
ALGORITHM = "HS256"


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    
    token = credentials.credentials

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        user_id = payload["id"]

    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = await users_collection.find_one({"_id": user_id})

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user