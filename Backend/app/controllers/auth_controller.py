from fastapi import HTTPException
from app.database import users_collection
from app.utils.security import hash_password, verify_password
from app.utils.jwt_handler import create_access_token


async def signup(user):

    existing_user = await users_collection.find_one({"email": user.email})

    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(user.password)

    new_user = {
        "name": user.name,
        "email": user.email,
        "password": hashed_password,
        "skills": user.skills
    }

    result = await users_collection.insert_one(new_user)

    token = create_access_token(str(result.inserted_id))

    return {
        "token": token,
        "user": {
            "id": str(result.inserted_id),
            "name": user.name,
            "email": user.email,
            "skills": user.skills
        }
    }


async def login(user):

    db_user = await users_collection.find_one({"email": user.email})

    if not db_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")

    if not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token(str(db_user["_id"]))

    return {
        "token": token,
        "user": {
            "id": str(db_user["_id"]),
            "name": db_user["name"],
            "email": db_user["email"],
            "skills": db_user["skills"]
        }
    }


async def logout():
    return {"message": "Logout successful"}