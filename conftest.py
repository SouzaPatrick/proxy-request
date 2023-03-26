from datetime import datetime

import pytest
from sqlmodel import Session, SQLModel

from app import models
from tests._factories import ExtractionMethodFactory, ProtocolFactory, ProxyFactory
from tests.database import engine


@pytest.fixture
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


@pytest.fixture
def protocol() -> models.Protocol:
    protocol_factory: models.Protocol = ProtocolFactory(name="fake_protocol")
    return protocol_factory


@pytest.fixture
def extraction_method(protocol) -> models.ExtractionMethod:
    extraction_method_factory: models.ExtractionMethod = ExtractionMethodFactory(
        name="fake_extraction_method",
        url="http://test.com",
        priority=0,
        method="fake_method",
        protocol_id=protocol.id,
        protocol=protocol,
    )
    return extraction_method_factory


@pytest.fixture
def proxy(extraction_method) -> models.Proxy:
    proxy_factory: models.Proxy = ProxyFactory(
        ip="0.0.0.0",
        port=80,
        status_check=True,
        ttl=30,
        last_check=datetime.now(),
        extraction_method_id=extraction_method.id,
        extraction_method=extraction_method,
    )
    return proxy_factory
