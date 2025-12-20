from datetime import datetime, timezone
from io import BytesIO
from typing import Self

import magic
from pydantic import BaseModel, Field, model_validator


class FileUpload(BaseModel):
    file_name: str
    create_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    file_size: int = 0
    description: str | None = None
    file_data: bytes
    mime_type: str = ""

    @model_validator(mode="after")
    def calculate_file_size(self) -> Self:
        if not self.file_size:
            print("calculate size")
            self.file_size = len(self.file_data)
        return self

    @model_validator(mode="after")
    def find_file_mime_type(self) -> Self:
        if not self.mime_type:
            print("find mime type")
            stream = BytesIO(self.file_data)
            self.mime_type = get_mime_type_from_stream(stream)
        return self


def get_mime_type_from_stream(data_stream: BytesIO):
    """
    Determines the MIME type of a file from its data stream.

    Args:
        data_stream: A file-like object (e.g., an open file or a BytesIO object)
                        representing the file's data.

    Returns:
        A string representing the MIME type, or None if it cannot be determined.
    """
    # Read a sufficient amount of data to allow libmagic to identify the type.
    # 2048 bytes is often a good starting point, but adjust as needed.
    buffer = data_stream.read(2048)

    if not buffer:
        return None  # Empty stream

    try:
        mime_type = magic.from_buffer(buffer, mime=True)
        return mime_type
    except magic.MagicException as e:
        print(f"Error determining MIME type: {e}")
        return None


if __name__ == "__main__":

    upload_file = UploadFile(file_name="test", file_data="سیسبasddafسب".encode())

    print(upload_file.file_size)
    print(upload_file.model_dump())


# class File(BaseModel):
#     file_name: str
#     url: str
#     create_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
#     file_size: int
#     description: str | None = None
#     file_data: bytes
