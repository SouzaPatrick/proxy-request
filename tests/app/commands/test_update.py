from datetime import datetime

from sqlmodel import select

from app.commands.update import update_proxy_status
from app.models import Proxy


def test_update(session, mocker):
    valid_proxies: list[Proxy] = [
        Proxy(
            ip="0.0.0.0", port=80, ttl=0, status_check=True, last_check=datetime.now()
        ),
        Proxy(
            ip="1.1.1.1", port=80, ttl=0, status_check=True, last_check=datetime.now()
        ),
        Proxy(
            ip="2.2.2.2", port=80, ttl=0, status_check=True, last_check=datetime.now()
        ),
        Proxy(
            ip="3.3.3.3", port=80, ttl=0, status_check=True, last_check=datetime.now()
        ),
    ]

    session.add_all(valid_proxies)

    query = select(Proxy)
    proxies: list[Proxy] = session.execute(query).scalars().all()

    assert proxies[0].status_check is True
    assert proxies[1].status_check is True
    assert proxies[2].status_check is True
    assert proxies[3].status_check is True

    mocker.patch(
        "app.commands.update.Proxy.get_all_valid_proxies", return_value=valid_proxies
    )
    mocker.patch("app.commands.update.proxy_request", return_value=False)

    update_proxy_status(session=session)

    query = select(Proxy)
    proxies: list[Proxy] = session.execute(query).scalars().all()

    assert proxies[0].status_check is False
    assert proxies[1].status_check is False
    assert proxies[2].status_check is False
    assert proxies[3].status_check is False
