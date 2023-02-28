from typing import NoReturn

import pytest
import requests
from proxy_request import ProxyRequest


@pytest.fixture
def proxy_request() -> ProxyRequest:
    _proxy_request: ProxyRequest = ProxyRequest()
    return _proxy_request


def test_init_default_values(proxy_request) -> NoReturn:
    assert proxy_request.destination_host == ""
    assert proxy_request.timeout == 10


def test_request_not_send_url(proxy_request) -> NoReturn:
    assert proxy_request.request(host_and_port="0.0.0.0:80") is None


@pytest.mark.parametrize("protocol", ["sock4", "sock5"])
def test_get_session_without_sending_the_protocol_as_http(
    proxy_request, protocol
) -> NoReturn:
    session: requests.Session = proxy_request._get_session(
        host_and_port="0.0.0.0:80", protocol=protocol
    )
    assert session.proxies == {
        "http": f"{protocol}://0.0.0.0:80",
        "https": f"{protocol}://0.0.0.0:80",
    }


def test_get_session_sending_the_protocol_as_http(proxy_request) -> NoReturn:
    session: requests.Session = proxy_request._get_session(
        host_and_port="0.0.0.0:80", protocol="http_https"
    )
    assert session.proxies == {"https": "0.0.0.0:80", "http": "0.0.0.0:80"}
