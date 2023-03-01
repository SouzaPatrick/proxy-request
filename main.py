from datetime import datetime

from app.db_functions import create_proxies, exist_proxy, get_extract_methods
from app.models import Proxy, ExtractionMethod
from app.utils.extract_proxy_list.search_method import search_method
from settings import TTL_PROXY
from app.utils.proxy_request import proxy_request

extract_methods: list[ExtractionMethod] = get_extract_methods()

for extract_method in extract_methods:
    proxies: list[str] = search_method(extract_method=extract_method)
    _proxies: list[Proxy] = []

    for proxy in proxies:
        # Check if the proxy already exists in the database, if it does, ignore the check
        proxy_ip, proxy_port = proxy.split(":")
        if not exist_proxy(ip=proxy_ip, port=int(proxy_port)):
            status_check: bool = proxy_request(proxy=proxy)

            proxy_ip, proxy_port = proxy.split(":")
            _proxies.append(
                Proxy(
                    ip=proxy_ip,
                    port=int(proxy_port),
                    status_check=status_check,
                    ttl=TTL_PROXY,
                    last_check=datetime.now(),
                    extraction_method_id=extract_method.id
                )
            )

    create_proxies(proxies=_proxies)
