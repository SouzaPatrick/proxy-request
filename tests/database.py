from sqlalchemy.future import Engine
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool


def get_engine() -> Engine:
    sqlite_file_name = "database_test.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"

    engine = create_engine(
        sqlite_url, connect_args={"check_same_thread": False}, poolclass=StaticPool
    )

    return engine


def get_session() -> Session:
    return Session(get_engine())
