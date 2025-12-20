from typing import Optional

import sqlalchemy
from sqlalchemy import create_engine

from web.app.settings import settings


def engine(connection_string: Optional[str] = None) -> sqlalchemy.engine.Engine:
    return create_engine(connection_string or settings.database.connection_string)
