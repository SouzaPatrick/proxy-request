from datetime import datetime

from sqlmodel import SQLModel

from app.models import ExtractionMethod, Protocol, Proxy


# Protocol
# -----------------------------------------------------------
def test_protocol_str():
    protocol: Protocol = Protocol(name="fake_protocol")
    assert str(protocol) == "<Protocol(name=fake_protocol)>"
    assert protocol.__repr__() == "<Protocol(name=fake_protocol)>"


def test_protocol_exists_success(session):
    protocol: Protocol = Protocol(name="fake_protocol")
    session.add(protocol)
    session.commit()

    protocol_exist: bool = Protocol.exists(session=session, name="fake_protocol")

    assert protocol_exist is True


def test_protocol_exists_not_found(session):
    protocol_exist: bool = Protocol.exists(session=session, name="fake_protocol")

    assert protocol_exist is False


def test_protocol_parent_class():
    assert issubclass(Protocol, SQLModel)


# Extraction Method
# -----------------------------------------------------------
def test_extraction_method_str():
    extraction_method: ExtractionMethod = ExtractionMethod(
        name="fake_extraction_method", url="", priority=0, method=""
    )
    assert str(extraction_method) == "<ExtractionMethod(name=fake_extraction_method)>"
    assert (
        extraction_method.__repr__()
        == "<ExtractionMethod(name=fake_extraction_method)>"
    )


def test_extraction_method_parent_class():
    assert issubclass(ExtractionMethod, SQLModel)


def test_extraction_method_exists_success(session):
    extraction_method: ExtractionMethod = ExtractionMethod(
        name="fake_extraction_method",
        url="http://test.com",
        priority=0,
        method="fake_method",
        protocol_id=1,
    )
    session.add(extraction_method)
    session.commit()

    extraction_method_exist: bool = ExtractionMethod.exists(
        session=session,
        name="fake_extraction_method",
        url="http://test.com",
        priority=0,
        method="fake_method",
        protocol_id=1,
    )

    assert extraction_method_exist is True


def test_extraction_method_exists_not_found(session):
    extraction_method_exists: bool = ExtractionMethod.exists(
        session=session,
        name="fake_extraction_method",
        url="http://test.com",
        priority=0,
        method="fake_method",
        protocol_id=1,
    )

    assert extraction_method_exists is False


# Proxy
# -----------------------------------------------------------
def test_proxy_str():
    proxy: Proxy = Proxy(ip="0.0.0.0", port=80, ttl=0, last_check=datetime.now())
    assert str(proxy) == "<Proxy(ip=0.0.0.0, port=80)>"
    assert proxy.__repr__() == "<Proxy(ip=0.0.0.0, port=80)>"


def test_proxy_parent_class():
    assert issubclass(Proxy, SQLModel)


def test_proxy_exists_success(session):
    last_check: datetime = datetime.now()
    proxy: Proxy = Proxy(ip="0.0.0.0", port=80, ttl=0, last_check=last_check)
    session.add(proxy)
    session.commit()

    proxy_exist: bool = Proxy.exists(
        session=session, ip="0.0.0.0", port=80, ttl=0, last_check=last_check
    )

    assert proxy_exist is True


def test_proxy_exists_not_found(session):
    proxy_exist: bool = Proxy.exists(
        session=session,
        ip="0.0.0.0",
        port=80,
        ttl=0,
        last_check=datetime.now(),
    )

    assert proxy_exist is False
