from app.db_functions import get_valid_proxies
from app.models import Proxy
from app.utils.proxy_request import proxy_request
from database import get_session

with get_session() as session:
    valid_proxies: list[Proxy] = get_valid_proxies(session=session)

for valid_proxy in valid_proxies:
    status_check: bool = proxy_request(proxy=f"{valid_proxy.ip}:{valid_proxy.port}")
    with get_session() as session:
        valid_proxy.update_status(session=session, status_check=status_check)
