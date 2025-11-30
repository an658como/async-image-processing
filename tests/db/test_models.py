from web.app.db.engine import engine
from web.app.db.models import Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

Session = sessionmaker(bind=engine)


class TestImages:
    def setup_class(self):
        Base.metadata.create_all(engine)
        self.session = Session()

    def teardown_class(self):
        self.session.rollback()
        self.session.close()

    def test_db_version(self):
        response = self.session.execute(text("SELECT version();")).scalar()
        assert "PostgreSQL" in response
