from sqlalchemy import create_engine
from web.app.settings import settings

engine = create_engine(settings.database.connection_string)
