import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session, SQLModel

load_dotenv()

database_url = os.getenv("DATABASE_URL")
if database_url is None:
    raise ValueError("DATABASE_URL environment variable is not set")

engine = create_engine(database_url, echo=True)


def create_db_and_tables():
    # SQLModel.metadata.drop_all(engine)  # Drop all tables
    SQLModel.metadata.create_all(engine)  # Create all tables


def get_session():
    with Session(engine) as session:
        yield session
