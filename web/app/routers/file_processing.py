from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, status
from web.app.file import FileUpload
from pathlib import Path
from uuid import uuid4
import logging

logging.basicConfig(level=logging.ERROR, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

file_router = APIRouter(prefix="/file")

upload_dir = Path(__file__).parent.parent / "temp" / "uploads"
upload_dir.mkdir(parents=True, exist_ok=True)


@file_router.post("/upload")
async def upload_file(file: UploadFile = File(...), description: Optional[str] = None):

    file_upload = FileUpload(
        file_name=file.filename,
        file_data=await file.read(),
        file_size=file.size,
        mime_type=file.content_type,
        description=description,
    )

    # save file
    try:
        temp_local_path = str(
            upload_dir / f"{str(uuid4().hex)}-{file_upload.file_name}"
        )
        with open(
            temp_local_path,
            "w",
        ) as f:
            f.write(file_upload.file_data)
        logger.info("File uploaded successfuly")
    except Exception as e:
        logger.exception("Failed to upload File :(")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save the file",
        )

    return {"upload": "successful", "path": temp_local_path}
