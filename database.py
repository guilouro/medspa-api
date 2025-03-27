from typing import Annotated
from fastapi import Depends
from sqlmodel import create_engine, SQLModel, Session
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)


def init_db():
    """
    Initialize the database and create all tables
    """
    SQLModel.metadata.create_all(engine)


def get_session():
    """
    Get a new session for the database
    """
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
