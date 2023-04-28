from datetime import datetime

from freezegun import freeze_time
from sqlmodel import select

from app.commands.console import console
from app.models import Proxy


@freeze_time("2023-01-01 08:41:38")
def test_console(session, extraction_method, mocker, capsys):
    valid_proxies: list[Proxy] = [
        Proxy(
            ip="0.0.0.0",
            port=80,
            ttl=0,
            status_check=True,
            last_check=datetime.now(),
            extraction_method_id=extraction_method.id,
        ),
        Proxy(
            ip="1.1.1.1",
            port=80,
            ttl=0,
            status_check=True,
            last_check=datetime.now(),
            extraction_method_id=extraction_method.id,
        ),
    ]

    session.add_all(valid_proxies)

    query = select(Proxy)
    proxies: list[Proxy] = session.execute(query).scalars().all()

    assert proxies[0].status_check is True
    assert proxies[1].status_check is True

    mocker.patch(
        "app.commands.console.Proxy.get_all_valid_proxies", return_value=valid_proxies
    )

    console(session=session)
    captured = capsys.readouterr()
    assert (
        captured.out
        == "                          Table of valid proxies                           \n"
        "                                                                           \n"
        "  Nº   PROXY        Url               Protocol        Last check           \n"
        " ───────────────────────────────────────────────────────────────────────── \n"
        "  0    0.0.0.0:80   http://test.com   fake_protocol   01/01/2023 08:41:38  \n"
        "  1    1.1.1.1:80   http://test.com   fake_protocol   01/01/2023 08:41:38  \n"
        "                                                                           \n"
    )
