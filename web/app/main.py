from contextlib import asynccontextmanager
from fastapi import FastAPI, UploadFile

from web.app.models import FileUpload
import logging

from web.app.routers.file_processing import file_router


from sqlalchemy.orm import Session, sessionmaker

from web.app.db.engine import engine
from web.app.db.models import Base


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)
SessionLocal = sessionmaker(bind=engine)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables (for dev)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(file_router)


@app.get("/")
def read_root():
    return {"Service": "Running"}


@app.post("/upload")
def upload_file(file: UploadFile, description: str):

    FileUpload(file_name=file.filename, file_data=file.file.read())
    return {"upload": "successful"}
