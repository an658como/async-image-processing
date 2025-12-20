import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text
from web.app.db.engine import engine as engine
from web.app.db.models import Base
from web.app.settings import settings


@pytest.fixture(scope="class")
def db_engine():
    eng = engine(
        f"postgresql://{settings.database.user}:{settings.database.password.get_secret_value()}@localhost:{settings.database.port}/{settings.database.name}"
    )
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
