from datetime import datetime

from sqlmodel import SQLModel

from app.models import BaseModel, ExtractionMethod, Protocol, Proxy
from tests._factories import ExtractionMethodFactory, ProtocolFactory, ProxyFactory


# Protocol
# -----------------------------------------------------------
def test_protocol_parent_class():
    assert issubclass(Protocol, SQLModel)
    assert issubclass(Protocol, BaseModel)


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


def test_protocol_get_by_fields(session):
    protocol_factory: Protocol = ProtocolFactory(name="fake_protocol")

    protocol: Protocol = Protocol.get_by_fields(session=session, name="fake_protocol")

    assert protocol_factory.id == protocol.id
    assert protocol_factory.created_at == protocol.created_at
    assert protocol_factory.name == protocol.name


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
    assert issubclass(ExtractionMethod, BaseModel)


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


def test_extraction_method_get_by_fields(session):
    protocol_factory: Protocol = ProtocolFactory(name="fake_protocol")
    extraction_method_factory: ExtractionMethod = ExtractionMethodFactory(
        name="fake_extraction_method",
        url="http://test.com",
        priority=0,
        method="fake_method",
        protocol_id=protocol_factory.id,
        protocol=protocol_factory,
    )

    extraction_method: ExtractionMethod = ExtractionMethod.get_by_fields(
        session=session,
        name="fake_extraction_method",
        url="http://test.com",
        priority=0,
        method="fake_method",
        protocol_id=protocol_factory.id,
        protocol=protocol_factory,
    )

    assert extraction_method_factory.id == extraction_method.id
    assert extraction_method_factory.created_at == extraction_method.created_at
    assert extraction_method_factory.name == extraction_method.name
    assert extraction_method_factory.url == extraction_method.url
    assert extraction_method_factory.priority == extraction_method.priority
    assert extraction_method_factory.method == extraction_method.method
    assert extraction_method_factory.protocol_id == extraction_method.protocol_id


def test_get_all_extraction_methods_sorted_by_priority(session, extraction_method):
    expected_result: list[ExtractionMethod] = [extraction_method]

    extract_methods: list[
        ExtractionMethod
    ] = ExtractionMethod.get_all_extraction_methods_sorted_by_priority(session)

    assert len(extract_methods) == 1
    assert extract_methods[0].id == expected_result[0].id
    assert extract_methods[0].created_at == expected_result[0].created_at
    assert extract_methods[0].name == expected_result[0].name
    assert extract_methods[0].url == expected_result[0].url
    assert extract_methods[0].priority == expected_result[0].priority
    assert extract_methods[0].method == expected_result[0].method
    assert extract_methods[0].protocol_id == expected_result[0].protocol_id


# Proxy

# -----------------------------------------------------------
def test_proxy_parent_class():
    assert issubclass(Proxy, SQLModel)
    assert issubclass(Proxy, BaseModel)


def test_proxy_str():
    proxy: Proxy = Proxy(ip="0.0.0.0", port=80, ttl=0, last_check=datetime.now())
    assert str(proxy) == "<Proxy(ip=0.0.0.0, port=80)>"
    assert proxy.__repr__() == "<Proxy(ip=0.0.0.0, port=80)>"


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


def test_proxy_get_by_fields(session):
    protocol_factory: Protocol = ProtocolFactory(name="fake_protocol")

    extraction_method_factory: ExtractionMethod = ExtractionMethodFactory(
        name="fake_extraction_method",
        url="http://test.com",
        priority=0,
        method="fake_method",
        protocol_id=protocol_factory.id,
        protocol=protocol_factory,
    )

    last_check: datetime = datetime.now()
    proxy_factory: Proxy = ProxyFactory(
        ip="0.0.0.0",
        port=80,
        status_check=True,
        ttl=30,
        last_check=last_check,
        extraction_method_id=extraction_method_factory.id,
        extraction_method=extraction_method_factory,
    )

    proxy: Proxy = Proxy.get_by_fields(
        session=session,
        ip="0.0.0.0",
        port=80,
        status_check=True,
        ttl=30,
        last_check=last_check,
        extraction_method_id=extraction_method_factory.id,
        extraction_method=extraction_method_factory,
    )

    assert proxy_factory.id == proxy.id
    assert proxy_factory.created_at == proxy.created_at
    assert proxy_factory.ip == proxy.ip
    assert proxy_factory.port == proxy.port
    assert proxy_factory.status_check == proxy.status_check
    assert proxy_factory.ttl == proxy.ttl
    assert proxy_factory.last_check == proxy.last_check
    assert proxy_factory.extraction_method_id == proxy.extraction_method_id
    assert proxy_factory.extraction_method == proxy.extraction_method


def test_get_all_valid_proxies(session):
    proxy: Proxy = ProxyFactory()
    expected_result: Proxy = proxy
    proxies: list[Proxy] = Proxy.get_all_valid_proxies(session=session)

    assert len(proxies) == 1
    assert proxies[0].id == expected_result.id
    assert proxies[0].ip == expected_result.ip
    assert proxies[0].status_check == expected_result.status_check
    assert proxies[0].port == expected_result.port
    assert proxies[0].last_check == expected_result.last_check


def test_get_all_valid_proxies_not_found(session):
    proxies: list[Proxy] = Proxy.get_all_valid_proxies(session=session)

    assert proxies == []


def test_update_status(session, proxy):
    proxy_factory = session.merge(proxy)

    assert proxy_factory.status_check is True

    proxy_factory.update_status(session=session, status_check=False)
    updated_proxy: Proxy = Proxy.get_by_fields(session=session, id=proxy_factory.id)

    assert updated_proxy.status_check is False
