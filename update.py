from typing import Optional

import requests

from app.check_proxy_request import CheckProxyRequest
from app.db_functions import get_valid_proxies, update_status_check_proxy
from app.models import Proxy
from settings import DESTINATION_HOST

valid_proxies: list[Proxy] = get_valid_proxies()
_proxies: list[Proxy] = []
for valid_proxy in valid_proxies:
    # Proxy validate
    try:
        proxy_request: Optional[requests.Response] = CheckProxyRequest(
            destination_host=DESTINATION_HOST
        ).request(host_and_port=f"{valid_proxy.ip}:{valid_proxy.port}")
    except:
        status_check: bool = False
        proxy_request: Optional[requests.Response] = None

    if proxy_request:
        status_check: bool = True
    else:
        status_check: bool = False

    update_status_check_proxy(proxy=valid_proxy, status_check=status_check)
