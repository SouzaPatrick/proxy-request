import requests

from app.utils.proxy_request import proxy_request


def test_proxy_request_success(mocker):
    mocker.patch(
        "app.utils.check_proxy_request.CheckProxyRequest.request", return_value="teste"
    )
    proxy_status_check: bool = proxy_request(proxy="")

    assert proxy_status_check is True


def test_proxy_request_when_the_check_return_None(mocker):
    mocker.patch(
        "app.utils.check_proxy_request.CheckProxyRequest.request", return_value=None
    )
    proxy_status_check: bool = proxy_request(proxy="")

    assert proxy_status_check is False


def test_proxy_error(mocker):
    mocker.patch(
        "app.utils.check_proxy_request.CheckProxyRequest.request",
        side_effect=requests.exceptions.ProxyError,
    )

    proxy_status_check: bool = proxy_request(proxy="")

    assert proxy_status_check is False


def test_proxy_connection_error(mocker):
    mocker.patch(
        "app.utils.check_proxy_request.CheckProxyRequest.request",
        side_effect=requests.exceptions.ConnectionError,
    )

    proxy_status_check: bool = proxy_request(proxy="")

    assert proxy_status_check is False


def test_proxy_timeout(mocker):
    mocker.patch(
        "app.utils.check_proxy_request.CheckProxyRequest.request",
        side_effect=requests.exceptions.Timeout,
    )

    proxy_status_check: bool = proxy_request(proxy="")

    assert proxy_status_check is False
