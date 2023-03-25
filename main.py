from datetime import datetime

from app.db_functions import create_proxies, get_extract_methods
from app.models import ExtractionMethod, Proxy
from app.utils.extract_proxy_list.search_method import search_method
from app.utils.proxy_request import proxy_request
from database import get_session
from settings import TTL_PROXY

extract_methods: list[ExtractionMethod] = get_extract_methods()

for extract_method in extract_methods:
    proxies: list[str] = search_method(
        method=extract_method.method, url=extract_method.url
    )
    _proxies: list[Proxy] = []

    for proxy in proxies:
        # Check if the proxy already exists in the database, if it does, ignore the check
        proxy_ip, proxy_port = proxy.split(":")
        with get_session() as session:
            if not Proxy.exists(session=session, ip=proxy_ip, port=int(proxy_port)):
                status_check: bool = proxy_request(proxy=proxy)

                proxy_ip, proxy_port = proxy.split(":")
                _proxies.append(
                    Proxy(
                        ip=proxy_ip,
                        port=int(proxy_port),
                        status_check=status_check,
                        ttl=TTL_PROXY,
                        last_check=datetime.now(),
                        extraction_method_id=extract_method.id,
                    )
                )

    create_proxies(proxies=_proxies)
