from datetime import datetime

from sqlmodel import Session, select

from app.commands.proxy import create_proxies
from app.models import ExtractionMethod, Proxy
from settings import TTL_PROXY


def test_create_proxies(session: Session, extraction_method: ExtractionMethod):
    _proxies: list[Proxy] = [
        Proxy(
            ip="1.1.1.1",
            port=8080,
            status_check=True,
            ttl=TTL_PROXY,
            last_check=datetime.now(),
            extraction_method_id=extraction_method.id,
        ),
        Proxy(
            ip="2.2.2.2",
            port=80,
            status_check=True,
            ttl=TTL_PROXY,
            last_check=datetime.now(),
            extraction_method_id=extraction_method.id,
        ),
    ]

    create_proxies(session=session, proxies=_proxies)

    query = select(Proxy)
    proxies: list[Proxy] = session.execute(query).scalars().all()

    assert len(proxies) == len(_proxies)
