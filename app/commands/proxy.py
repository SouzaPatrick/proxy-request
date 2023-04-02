from datetime import datetime
from typing import NoReturn

from sqlmodel import Session

from app.models import ExtractionMethod, Proxy
from app.utils.extract_proxy_list.search_method import search_method
from app.utils.proxy_request import proxy_request
from settings import TTL_PROXY


def create_proxies(session: Session, proxies: list[Proxy]) -> NoReturn:
    for proxy in proxies:
        session.add(proxy)
        session.commit()


def proxy(session: Session) -> NoReturn:
    extract_methods: list[
        ExtractionMethod
    ] = ExtractionMethod.get_all_extraction_methods_sorted_by_priority(session)

    for extract_method in extract_methods:
        proxies: list[str] = search_method(
            method=extract_method.method, url=extract_method.url
        )
        _proxies: list[Proxy] = []

        for proxy in proxies:
            # Check if the proxy already exists in the database, if it does, ignore the check
            proxy_ip, proxy_port = proxy.split(":")

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

        create_proxies(session=session, proxies=_proxies)
