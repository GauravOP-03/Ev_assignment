from fastapi import Header, HTTPException
from jose import jwt
from db.mongo import users_collection
from dotenv import load_dotenv
load_dotenv()
import os
AUTH_SECRET = os.getenv("AUTH_SECRET", "auth_secret") 
AUTH_ALGORITHM = "HS256"

# Generate JWT Token
def create_token(user: dict) -> str:
    payload = {
        "email": user["email"],
        "user_type": user["user_type"]
    }
    return jwt.encode(payload, AUTH_SECRET, algorithm=AUTH_ALGORITHM)

# Validate JWT and get user info
async def get_current_user(token: str = Header(...)) -> dict:
    try:
        payload = jwt.decode(token, AUTH_SECRET, algorithms=[AUTH_ALGORITHM])
        email = payload.get("email")

        user = await users_collection.find_one({"email": email})
        if not user or (user["user_type"] == "client" and not user.get("is_verified", False)):
            raise HTTPException(status_code=403, detail="User not verified or not found")

        return {
            "email": user["email"],
            "user_type": user["user_type"]
        }

    except jwt.JWTError:
        raise HTTPException(status_code=403, detail="Invalid or expired token")

# Guard: Only Ops Users
def is_ops_user(user: dict):
    if user.get("user_type") != "ops":
        raise HTTPException(status_code=403, detail="Only Ops user allowed")

# Guard: Only Client Users
def is_client_user(user: dict):
    if user.get("user_type") != "client":
        raise HTTPException(status_code=403, detail="Only Client user allowed")