from typing import Optional

import requests
from rich.console import Console

from app.utils.check_proxy_request import CheckProxyRequest
from settings import DESTINATION_HOST

console: Console = Console()


def proxy_request(proxy: str, protocol: str = 'http') -> bool:
    try:
        _proxy_request: Optional[requests.Response] = CheckProxyRequest(
            destination_host=DESTINATION_HOST
        ).request(proxy=proxy, protocol=protocol)
    except Exception as error:
        console.log(str(error))
        _proxy_request: Optional[requests.Response] = None

    if _proxy_request:
        proxy_status_check: bool = True
        console.log(f"[b][white on green]{proxy}[/][/b]")
    else:
        proxy_status_check: bool = False
        console.log(f"[red]{proxy}[/red]")

    return proxy_status_check
