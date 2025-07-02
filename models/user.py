from pydantic import BaseModel, EmailStr
from typing import Optional

# For signup input
class User(BaseModel):
    email: EmailStr
    password: str
    user_type: str = "client"  # 'ops' or 'client'
    is_verified: Optional[bool] = False