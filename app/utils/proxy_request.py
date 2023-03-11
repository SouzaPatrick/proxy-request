from typing import Optional

import requests
from requests.exceptions import ProxyError, Timeout
from rich.console import Console

from app.utils.check_proxy_request import CheckProxyRequest
from settings import DESTINATION_HOST

console: Console = Console()


def proxy_request(proxy: str, protocol: str = "http") -> bool:
    try:

        response: Optional[requests.Response] = CheckProxyRequest(
            destination_host=DESTINATION_HOST
        ).request(proxy=proxy, protocol=protocol)
        if response:
            proxy_status_check: bool = True
        else:
            proxy_status_check: bool = False
    except ProxyError:
        proxy_status_check: bool = False
    except Timeout:
        proxy_status_check: bool = False

    if proxy_status_check:
        console.log(f"[b][white on green]{proxy}[/][/b]")
    else:
        console.log(f"[red]{proxy}[/red]")

    return proxy_status_check
