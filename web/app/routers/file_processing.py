import json
import logging
from pathlib import Path
from typing import Optional
from uuid import uuid4

import pika
from fastapi import APIRouter, File, HTTPException, UploadFile, status
from sqlalchemy.orm import Session, sessionmaker

from ..db.engine import engine
from ..db.models import Image
from ..services.object_store import cloud_client, get_object_store
from ..settings import settings

SessionLocal = sessionmaker(bind=engine())

logging.basicConfig(level=logging.ERROR, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

file_router = APIRouter(prefix="/file")

object_store = get_object_store(settings.cloud_provider)(cloud_client(settings.minio))


# message queue defintion
connection = pika.BlockingConnection(pika.ConnectionParameters("host.docker.internal"))
channel = connection.channel()
channel.queue_declare(queue="incoming_image")


@file_router.post("/upload")
async def upload_file(
    file: UploadFile = File(...), user_id: int = 1, description: Optional[str] = None
):
    key = f"user_{user_id}/{str(uuid4().hex)}-{file.filename}"

    # Insert DB record
    db: Session = SessionLocal()
    image_record = Image(
        user_id=user_id,
        filename=file.filename,
        filesize=file.size,
        description=description,
        status="pending",
        object_store_key=key,
    )
    db.add(image_record)
    db.commit()
    db.refresh(image_record)

    # save file
    try:
        object_store.upload_file(
            bucket_name=settings.object_store.incoming,
            key=key,
            data=file.file,
        )
        logger.info("File uploaded successfuly")

        message = {
            "image_id": image_record.id,
            "bucket": settings.object_store.incoming,
            "key": key,
        }

        # send a message to the queue
        channel.basic_publish(
            exchange="", routing_key="incoming_image", body=json.dumps(message).encode()
        )
        logger.info("A message is sent to the queue")
    except Exception as e:
        db.rollback()
        logger.exception("Failed to upload File :(")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save the file",
        )
    finally:
        db.close()

    # create a message and send it to the broker

    return {"upload": "successful"}


# debug end-point - needs to be removed later
@file_router.get("/debug/get-messages")
def debug_get_messages(limit: int = 10):
    """
    DEBUG ONLY.
    Reads up to `limit` messages from RabbitMQ and ACKs them.
    Do NOT use in production.
    """

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="host.docker.internal")
    )
    channel = connection.channel()

    messages = []

    for _ in range(limit):
        method_frame, header_frame, body = channel.basic_get(
            queue="incoming_image",
            auto_ack=True,  # IMPORTANT
        )

        if method_frame is None:
            break

        messages.append(body.decode())

    connection.close()

    return {
        "count": len(messages),
        "messages": messages,
    }
