from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from models.user import User
from db.mongo import users_collection, files_collection
from utils.token import create_email_token, verify_email_token
from utils.auth import create_token, get_current_user, is_client_user
from utils.email import send_verification_email
from utils.encrypt import generate_secure_url, verify_secure_url
import bcrypt

router = APIRouter()

@router.post("/signup")
async def signup(user: User):
    existing = await users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    token = create_email_token(user.email)
    await users_collection.insert_one({
        "email": user.email,
        "password": hashed_pw.decode(),
        "is_verified": False,
        "user_type": "client"
    })

    await send_verification_email(user.email, token)
    return {"message": "Check your email to verify your account."}

@router.get("/verify-email")
async def verify_email(token: str):
    email = verify_email_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    result = await users_collection.update_one({"email": email}, {"$set": {"is_verified": True}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return HTMLResponse("<h1>Email Verified! You can now login.</h1>")

@router.get("/download-file/{file_id}")
async def get_download_link(file_id: str, user=Depends(get_current_user)):
    is_client_user(user)
    secure_id = generate_secure_url(file_id, user["email"])
    return {
        "download-link": f"/client/download/{secure_id}",
        "message": "success"
    }

@router.get("/download/{secure_id}")
async def download_file(secure_id: str, user=Depends(get_current_user)):
    is_client_user(user)
    file_name = verify_secure_url(secure_id, user["email"])
    file_path = f"files/{file_name}"
    return FileResponse(path=file_path, filename=file_name)

@router.get("/files")
async def list_uploaded_files(user=Depends(get_current_user)):
    is_client_user(user)
    files = await files_collection.find().to_list(100)
    return {
        "count": len(files),
        "files": [{"filename": f["filename"], "file_id": f["file_id"]} for f in files]
    }

router = APIRouter()

@router.post("/signup")
async def signup(user: User):
    existing = await users_collection.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pw = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    token = create_email_token(user.email)
    await users_collection.insert_one({
        "email": user.email,
        "password": hashed_pw.decode(),
        "is_verified": False,
        "user_type": "client"
    })

    await send_verification_email(user.email, token)
    return {"message": "Check your email to verify your account."}

@router.get("/verify-email")
async def verify_email(token: str):
    email = verify_email_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    result = await users_collection.update_one({"email": email}, {"$set": {"is_verified": True}})
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="User not found")

    return HTMLResponse("<h1>Email Verified! You can now login.</h1>")

@router.get("/download-file/{file_id}")
async def get_download_link(file_id: str, user=Depends(get_current_user)):
    is_client_user(user)
    secure_id = generate_secure_url(file_id, user["email"])
    return {
        "download-link": f"/client/download/{secure_id}",
        "message": "success"
    }

@router.get("/download/{secure_id}")
async def download_file(secure_id: str, user=Depends(get_current_user)):
    is_client_user(user)
    file_name = verify_secure_url(secure_id, user["email"])
    file_path = f"files/{file_name}"
    return FileResponse(path=file_path, filename=file_name)

@router.get("/files")
async def list_uploaded_files(user=Depends(get_current_user)):
    is_client_user(user)
    files = await files_collection.find().to_list(100)
    return {
        "count": len(files),
        "files": [{"filename": f["filename"], "file_id": f["file_id"]} for f in files]
    }