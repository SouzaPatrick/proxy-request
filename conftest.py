import pytest
from sqlmodel import Session, SQLModel

from app import models
from tests.database import engine


@pytest.fixture()
def db_setup():

    """Creates a database engine in memory."""
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
    with Session(engine) as session:
        yield session
