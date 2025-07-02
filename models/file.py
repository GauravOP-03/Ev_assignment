from pydantic import BaseModel
from typing import Optional

class FileMetadata(BaseModel):
    file_id: str
    filename: str
    uploader: str