from typing import Optional

from app.db_functions import get_protocol_with_id, get_valid_proxies
from app.models import Protocol, Proxy
from tests._factories import ProtocolFactory, ProxyFactory


def test_get_valid_proxies(session):
    proxy: Proxy = ProxyFactory()
    expected_result: Proxy = proxy
    proxies: list[Proxy] = get_valid_proxies(session=session)

    assert len(proxies) == 1
    assert proxies[0].id == expected_result.id
    assert proxies[0].ip == expected_result.ip
    assert proxies[0].status_check == expected_result.status_check
    assert proxies[0].port == expected_result.port
    assert proxies[0].last_check == expected_result.last_check


def test_get_valid_proxies_not_found(session):
    proxies: list[Proxy] = get_valid_proxies(session=session)

    assert proxies == []


def test_get_protocol_with_id(session):
    protocol: Protocol = ProtocolFactory()
    protocol_found: Optional[Protocol] = get_protocol_with_id(
        session=session, protocol_id=protocol.id
    )

    assert protocol.id == protocol_found.id
    assert protocol.name == protocol_found.name
