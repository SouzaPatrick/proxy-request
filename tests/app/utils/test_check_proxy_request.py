from typing import NoReturn
from unittest.mock import patch

import pytest
import requests
from requests import Session

from app.utils.check_proxy_request import CheckProxyRequest


@pytest.fixture(scope="session")
def proxy_request() -> CheckProxyRequest:
    _proxy_request: CheckProxyRequest = CheckProxyRequest(timeout=10)
    return _proxy_request


class MockResponse:
    def __init__(
        self,
        status_code: int = 200,
        content: str = "Mock content",
        text: str = "Mock text",
        json: dict = {},
    ):
        self.status_code = status_code
        self.content = content
        self.text = text
        self.json = json


def test_init_default_values(proxy_request: CheckProxyRequest) -> NoReturn:
    assert proxy_request.destination_host == ""
    assert proxy_request.timeout == 10


def test_request_not_send_url(proxy_request: CheckProxyRequest) -> NoReturn:
    assert proxy_request.request(proxy="0.0.0.0:80", protocol="http") is None


@patch.object(Session, "get")
def test_request_success(mock_get) -> NoReturn:
    proxy_request: CheckProxyRequest = CheckProxyRequest(
        destination_host="http://google.com"
    )
    mock_get.return_value = MockResponse(
        status_code=200, content="Mock content", text="Mock text", json={}
    )

    response = proxy_request.request(proxy="0.0.0.0:80", protocol="http")
    assert response.status_code == 200
    assert response.text == "Mock text"
    assert response.content == "Mock content"
    assert response.json == {}


@pytest.mark.parametrize("protocol", ["sock4", "sock5"])
def test_get_session_without_sending_the_protocol_as_http(
    proxy_request: CheckProxyRequest, protocol: str
) -> NoReturn:
    session: requests.Session = proxy_request._get_session(
        proxy="0.0.0.0:80", protocol=protocol
    )
    assert session.proxies == {
        "http": f"{protocol}://0.0.0.0:80",
        "https": f"{protocol}://0.0.0.0:80",
    }


def test_get_session_sending_the_protocol_as_http(
    proxy_request: CheckProxyRequest,
) -> NoReturn:
    session: requests.Session = proxy_request._get_session(
        proxy="0.0.0.0:80", protocol="http"
    )
    assert session.proxies == {"https": "0.0.0.0:80", "http": "0.0.0.0:80"}
