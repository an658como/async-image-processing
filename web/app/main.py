from fastapi import FastAPI, UploadFile

from web.app.file import FileUpload
import logging

from web.app.routers.file_processing import file_router

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(file_router)


@app.get("/")
def read_root():
    return {"Service": "Running"}


@app.post("/upload")
def upload_file(file: UploadFile, description: str):

    FileUpload(file_name=file.filename, file_data=file.file.read())
    return {"upload": "successful"}
