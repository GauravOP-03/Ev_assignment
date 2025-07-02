import time, hmac, hashlib, base64
from fastapi import HTTPException
from dotenv import load_dotenv
load_dotenv()
import os
URL_SECRET = os.getenv("URL_SECRET", "url-secret-key").encode()

def generate_secure_url(file_id: str, email: str):
    ts = str(int(time.time()))
    data = f"{file_id}|{email}|{ts}"
    sig = hmac.new(URL_SECRET, data.encode(), hashlib.sha256).hexdigest()
    raw = f"{data}|{sig}"
    return base64.urlsafe_b64encode(raw.encode()).decode()

def verify_secure_url(token: str, email: str):
    try:
        decoded = base64.urlsafe_b64decode(token).decode()
        file_id, token_email, ts, sig = decoded.split("|")
        if token_email != email:
            raise Exception("Invalid user")
        expected_sig = hmac.new(URL_SECRET, f"{file_id}|{email}|{ts}".encode(), hashlib.sha256).hexdigest()
        if sig != expected_sig:
            raise Exception("Invalid signature")
        if int(time.time()) - int(ts) > 600:
            raise Exception("Link expired")
        return file_id
    except Exception as e:
        raise HTTPException(status_code=403, detail=str(e))