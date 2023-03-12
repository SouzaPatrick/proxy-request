from typing import NoReturn

from sqlalchemy.future import Engine
from sqlmodel import Session, SQLModel, create_engine


def get_engine() -> Engine:
    sqlite_file_name = "database.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    engine = create_engine(sqlite_url)

    return engine


def get_session() -> Session:
    engine: Engine = get_engine()
    return Session(engine)


def create_db_and_tables() -> NoReturn:
    from app import models

    engine: Engine = get_engine()
    SQLModel.metadata.create_all(engine)
