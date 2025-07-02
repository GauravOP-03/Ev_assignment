from aiosmtplib import send
from email.message import EmailMessage
import os
from dotenv import load_dotenv
load_dotenv()

SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")  

async def send_verification_email(to_email: str, token: str):
    message = EmailMessage()
    message["From"] = SMTP_USER
    message["To"] = to_email
    message["Subject"] = "Verify your email"
    message.set_content(f"Click the link to verify: http://localhost:8000/client/verify-email?token={token}")
    
    await send(message, hostname="smtp.gmail.com", port=587, start_tls=True, username=SMTP_USER, password=SMTP_PASS)