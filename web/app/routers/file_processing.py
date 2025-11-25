from fastapi import APIRouter, UploadFile
from web.app.file import FileUpload

file_router = APIRouter(prefix="/file")


@file_router.post("/upload")
def upload_file(file: UploadFile, description: str):

    file_upload = FileUpload(
        file_name=file.filename,
        file_data=file.file.read(),
        file_size=file.size,
        mime_type=file.content_type,
    )
    return {"upload": "successful"}
