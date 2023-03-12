from sqlalchemy.future import Engine
from sqlmodel import create_engine


def get_engine() -> Engine:
    sqlite_file_name = "database_test.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    engine = create_engine(sqlite_url)

    return engine
