from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from db.mongo import users_collection
from utils.auth import create_token
import bcrypt

router = APIRouter()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/login")
async def login_user(payload: LoginRequest):
    # Find user by email
    user = await users_collection.find_one({"email": payload.email})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Check password
    if not bcrypt.checkpw(payload.password.encode(), user["password"].encode()):
        raise HTTPException(status_code=401, detail="Invalid password")

    # For client user, verify email
    if user["user_type"] == "client" and not user.get("is_verified", False):
        raise HTTPException(status_code=403, detail="Email not verified")

    # Create JWT token
    token = create_token(user)

    return {
        "access_token": token,
        "user_type": user["user_type"]
    }

