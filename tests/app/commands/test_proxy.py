from datetime import datetime

from freezegun import freeze_time
from sqlmodel import Session, select

from app.commands.proxy import create_proxies, proxy
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


@freeze_time("2023-01-01 08:41:38")
def test_proxy(session, mocker, extraction_method: ExtractionMethod):
    mocker.patch(
        "app.commands.proxy.ExtractionMethod.get_all_extraction_methods_sorted_by_priority",
        return_value=[extraction_method],
    )
    mocker.patch(
        "app.commands.proxy.search_method",
        return_value=["1.1.1.1:8080"],
    )
    mocker.patch(
        "app.commands.proxy.proxy_request",
        return_value=True,
    )

    proxy(session)

    query = select(Proxy)
    proxies: list[Proxy] = session.execute(query).scalars().all()

    assert len(proxies) == 1
    assert proxies[0].port == 8080
    assert proxies[0].status_check is True
    assert proxies[0].ttl == TTL_PROXY
    assert proxies[0].last_check == datetime.now()
    assert proxies[0].extraction_method_id == extraction_method.id
