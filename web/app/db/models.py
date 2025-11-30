from sqlalchemy import Column, Integer, String, Text, TIMESTAMP
from datetime import datetime, timezone
import sqlalchemy.orm

Base = sqlalchemy.orm.declarative_base()


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, nullable=False)
    filename = Column(Text, nullable=False)
    filesize = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    minio_key = Column(Text, nullable=True)  # will be filled later
    status = Column(String(20), default="pending")
    created_at = Column(TIMESTAMP, default=datetime.now(timezone.utc))
    updated_at = Column(
        TIMESTAMP,
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc),
    )
