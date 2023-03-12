import pytest
from sqlalchemy.future import Engine
from sqlmodel import Session, SQLModel

from app import models
from tests._factories import ProtocolFactory
from tests.database import get_engine


@pytest.fixture()
def db_setup():
    """Creates a database engine in memory."""
    engine: Engine = get_engine()
    SQLModel.metadata.create_all(engine)
    yield
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="session")
def session_fixture(db_setup):
    """
    Creates a database session for the function only,
    rollingback all commit to keep the test database
    always clean
    """
    engine: Engine = get_engine()

    with Session(engine) as session:
        yield session


@pytest.fixture
def protocol(db_setup):
    return ProtocolFactory()
