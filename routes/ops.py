from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from utils.auth import get_current_user, is_ops_user
from db.mongo import files_collection
import shutil
from uuid import uuid4
import os

router = APIRouter()

# Allowed MIME types
ALLOWED_MIME_TYPES = {
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # .docx
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",       # .xlsx
    "application/vnd.openxmlformats-officedocument.presentationml.presentation" # .pptx
}

UPLOAD_DIR = "files"

@router.post("/upload-file")
async def upload_file(
    file: UploadFile = File(...),
    user: dict = Depends(get_current_user)
):
    # Ensure only ops users can access
    is_ops_user(user)

    if file.content_type not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only .docx, .xlsx, and .pptx are allowed."
        )

    file_id = str(uuid4())
    saved_name = f"{file_id}_{file.filename}"
    file_path = os.path.join(UPLOAD_DIR, saved_name)

    # Ensure the 'files' directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    try:
        with open(file_path, "wb") as f:
            shutil.copyfileobj(file.file, f)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"File upload failed: {str(e)}"
        )

    # Save metadata to DB
    await files_collection.insert_one({
        "file_id": saved_name,
        "filename": file.filename,
        "uploader": user["email"]
    })

    return {
        "message": "File uploaded successfully",
        "file_id": saved_name
    }
