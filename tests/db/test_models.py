import pytest
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from web.app.db.engine import engine as engine
from web.app.db.models import Base
from web.app.settings import Settings, settings


@pytest.fixture
def test_settings() -> Settings:
    settings.database.host = "localhost"
    return settings


@pytest.fixture()
def db_engine(test_settings):
    eng = engine(test_settings.database.connection_string)
    Base.metadata.create_all(eng)
    yield eng
    eng.dispose()


@pytest.fixture
def db_session(db_engine):
    Session = sessionmaker(bind=db_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


class TestImages:
    def test_db_version(self, db_session):
        response = db_session.execute(text("SELECT version();")).scalar()
        assert "PostgreSQL" in response
