import logging
from contextlib import asynccontextmanager

import boto3
from fastapi import FastAPI, UploadFile
from sqlalchemy.orm import sessionmaker

from web.app.models import FileUpload
from web.app.routers.file_processing import file_router

from .db.engine import engine
from .db.models import Base
from .services.object_store import ObjectStore
from .settings import settings

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

db_engine = engine()
SessionLocal = sessionmaker(bind=db_engine)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.minio.admin_user,
    aws_secret_access_key=settings.minio.admin_password,
    endpoint_url=settings.minio.endpoint,
)

object_store = ObjectStore(s3_client)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables (for dev)
    Base.metadata.create_all(bind=db_engine)

    # get bucket names
    bucket_names = object_store.bucket_names()

    # create buckets
    object_store.create_buckets(
        bucket_names=settings.object_store.bucket_names.difference(bucket_names)
    )

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(file_router)


@app.get("/")
def read_root():
    print("Hello world!")
    return {"Service": "Running"}


@app.post("/upload")
def upload_file(file: UploadFile, description: str):

    FileUpload(file_name=file.filename, file_data=file.file.read())
    return {"upload": "successful"}
