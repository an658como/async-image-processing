import logging
from pathlib import Path
from typing import Optional
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session, sessionmaker

from web.app.models import FileUpload

from ..db.engine import engine
from ..db.models import Image
from ..services.object_store import cloud_client, get_object_store
from ..settings import settings

SessionLocal = sessionmaker(bind=engine())

logging.basicConfig(level=logging.ERROR, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

file_router = APIRouter(prefix="/file")

object_store = get_object_store(settings.cloud_provider)(cloud_client(settings.minio))


@file_router.post("/upload")
async def upload_file(
    file: UploadFile = File(...), user_id: int = 1, description: Optional[str] = None
):

    file_upload = FileUpload(
        file_name=file.filename,
        file_data=await file.read(),
        file_size=file.size,
        mime_type=file.content_type,
        description=description,
    )

    # save file
    try:
        key = f"{str(uuid4().hex)}-{file_upload.file_name}"
        object_store.upload_file(
            bucket_name=settings.object_store.incoming,
            key=key,
            data=file_upload.file_data,
        )
        logger.info("File uploaded successfuly")
    except Exception as e:
        logger.exception("Failed to upload File :(")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save the file",
        )

    # Insert DB record
    db: Session = SessionLocal()
    image_record = Image(
        user_id=user_id,
        filename=file_upload.file_name,
        filesize=file_upload.file_size,
        description=file_upload.description,
        status="pending",
    )
    db.add(image_record)
    db.commit()
    db.refresh(image_record)

    # create a message and send it to the broker

    return {"upload": "successful"}
