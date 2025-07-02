from jose import jwt, JWTError
import time
from dotenv import load_dotenv
load_dotenv()
import os
SECRET_KEY = os.getenv("AUTH_SECRET", "auth_secret")  
ALGORITHM = "HS256"
EXPIRE_TIME = 1800  # 30 mins

def create_email_token(email: str) -> str:
    payload = {"email": email, "exp": time.time() + EXPIRE_TIME}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_email_token(token: str) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload["email"]
    except JWTError:
        return None
