from app.db_functions import get_valid_proxies, update_status_check_proxy
from app.models import Proxy
from app.utils.proxy_request import proxy_request

valid_proxies: list[Proxy] = get_valid_proxies()
_proxies: list[Proxy] = []
for valid_proxy in valid_proxies:
    update_status_check_proxy(
        proxy=valid_proxy,
        status_check=proxy_request(proxy=f"{valid_proxy.ip}:{valid_proxy.port}"),
    )
