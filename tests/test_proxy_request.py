from typing import NoReturn

import pytest
import requests
from app.utils.check_proxy_request import CheckProxyRequest


@pytest.fixture
def proxy_request() -> CheckProxyRequest:
    _proxy_request: CheckProxyRequest = CheckProxyRequest()
    return _proxy_request


def test_init_default_values(proxy_request) -> NoReturn:
    assert proxy_request.destination_host == ""
    assert proxy_request.timeout == 10


def test_request_not_send_url(proxy_request) -> NoReturn:
    assert proxy_request.request(proxy="0.0.0.0:80", protocol="http") is None


@pytest.mark.parametrize("protocol", ["sock4", "sock5"])
def test_get_session_without_sending_the_protocol_as_http(
    proxy_request, protocol
) -> NoReturn:
    session: requests.Session = proxy_request._get_session(
        proxy="0.0.0.0:80", protocol=protocol
    )
    assert session.proxies == {
        "http": f"{protocol}://0.0.0.0:80",
        "https": f"{protocol}://0.0.0.0:80",
    }


def test_get_session_sending_the_protocol_as_http(proxy_request) -> NoReturn:
    session: requests.Session = proxy_request._get_session(
        proxy="0.0.0.0:80", protocol="http"
    )
    assert session.proxies == {"https": "0.0.0.0:80", "http": "0.0.0.0:80"}
