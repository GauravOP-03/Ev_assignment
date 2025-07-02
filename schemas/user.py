from pydantic import BaseModel, EmailStr

class User(BaseModel):
    email: EmailStr
    password: str
    is_verified: bool = False
    user_type: str  # "ops" or "client"