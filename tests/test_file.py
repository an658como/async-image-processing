from unittest.mock import patch

import magic
import pytest
from pydantic import ValidationError

from web.app.models import FileUpload


def test_upload_file_missing_required_fields():
    with pytest.raises(ValidationError) as exc:
        FileUpload()

    error_fields = {tuple(err["loc"]) for err in exc.value.errors()}
    assert ("file_name",) in error_fields
    assert ("file_data",) in error_fields


def test_upload_file_creation():
    file_name = "example.txt"
    file_data = b"Hello, World!"
    description = "Sample file"

    upload_file = FileUpload(
        file_name=file_name, file_data=file_data, description=description
    )

    assert isinstance(upload_file, FileUpload)
    assert upload_file.file_name == file_name
    assert upload_file.file_data == file_data
    assert upload_file.description == description
    assert upload_file.file_size == len(file_data)
    assert upload_file.mime_type == "text/plain"


def test_pdf_upload_file_creation():
    file_name = "example.pdf"
    # PDF file header bytes
    file_data = b"%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n"
    description = "Sample PDF file"

    upload_file = FileUpload(
        file_name=file_name, file_data=file_data, description=description
    )

    assert upload_file.mime_type.startswith("application/")
    assert "pdf" in upload_file.mime_type


def test_jpeg_upload_file_creation():
    file_name = "example.jpg"
    # JPEG file header bytes
    file_data = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x02"
    description = "Sample JPEG file"

    upload_file = FileUpload(
        file_name=file_name, file_data=file_data, description=description
    )

    assert upload_file.mime_type.startswith("image/")
    assert "jpeg" in upload_file.mime_type or "jpg" in upload_file.mime_type


def test_empty_file_data_sets_mime_to_none():
    f = FileUpload(file_name="empty.txt", file_data=b"")
    assert f.file_size == 0
    assert f.mime_type is None


def test_magic_exception_results_in_none():
    with patch(
        "web.app.models.magic.from_buffer", side_effect=magic.MagicException("fail")
    ):
        f = FileUpload(file_name="x", file_data=b"123")
        assert f.mime_type is None
