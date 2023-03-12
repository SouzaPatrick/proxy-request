import pytest
from sqlalchemy.future import Engine
from sqlmodel import Session, SQLModel

from tests.database import get_engine


@pytest.fixture(scope="session")
def db_setup():
    """Creates a database engine in memory."""
    from app import models

    engine: Engine = get_engine()

    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(db_setup):
    """
    Creates a database session for the function only,
    rollingback all commit to keep the test database
    always clean
    """
    engine: Engine = get_engine()

    transaction = engine.connect().begin()

    session: Session = Session(engine)

    yield session

    session.close()

    transaction.rollback()
