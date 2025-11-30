from typing import Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, status
from web.app.models import FileUpload
from pathlib import Path
from uuid import uuid4
import logging

from sqlalchemy.orm import Session, sessionmaker

from web.app.db.engine import engine
from web.app.db.models import Image, Base

SessionLocal = sessionmaker(bind=engine)
# Create tables (for dev)
Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.ERROR, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

file_router = APIRouter(prefix="/file")

upload_dir = Path(__file__).parent.parent / "temp" / "uploads"
upload_dir.mkdir(parents=True, exist_ok=True)


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
        temp_local_path = str(
            upload_dir / f"{str(uuid4().hex)}-{file_upload.file_name}"
        )
        with open(
            temp_local_path,
            "wb",
        ) as f:
            f.write(file_upload.file_data)
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

    return {"upload": "successful", "path": temp_local_path}
