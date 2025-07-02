from models.file import FileMetadata

# In file listing response:
async def list_files():
    files = await files_collection.find().to_list(100)
    return {
        "count": len(files),
        "files": [FileMetadata(**f) for f in files]
    }