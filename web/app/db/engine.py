from typing import Optional
from sqlalchemy import create_engine
import sqlalchemy
from web.app.settings import settings


def engine(connection_string: Optional[str] = None) -> sqlalchemy.engine.Engine:
    return create_engine(connection_string or settings.database.connection_string)
