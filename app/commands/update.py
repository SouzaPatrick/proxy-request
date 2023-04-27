from sqlmodel import Session

from app.models import Proxy
from app.utils.proxy_request import proxy_request


def update_proxy_status(session: Session) -> None:
    valid_proxies: list[Proxy] = Proxy.get_all_valid_proxies(session=session)

    for valid_proxy in valid_proxies:
        status_check: bool = proxy_request(proxy=f"{valid_proxy.ip}:{valid_proxy.port}")

        valid_proxy.update_status(session=session, status_check=status_check)
