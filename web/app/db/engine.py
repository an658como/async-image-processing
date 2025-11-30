import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

# db config:
DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@localhost:5432/images"
engine = create_engine(DB_URL)
