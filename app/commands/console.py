from typing import NoReturn, Optional

from rich import box, print
from rich.table import Table
from sqlmodel import Session

from app.models import Protocol, Proxy
from database import get_session


def console(session: Session) -> NoReturn:
    table = Table(title="Table of valid proxies", box=box.SIMPLE)
    table.add_column("Nº")
    table.add_column("PROXY")
    table.add_column("Url")
    table.add_column("Protocol")
    table.add_column("Last check")

    with get_session() as session:
        proxies: Optional[list[Proxy]] = Proxy.get_all_valid_proxies(session=session)

    for index, proxy in enumerate(proxies):
        with get_session() as session:
            import ipdb

            ipdb.set_trace()
            protocol_name: str = Protocol.get_by_fields(
                session=session, id=proxy.extraction_method.protocol_id
            ).name
        table.add_row(
            str(index),
            f"{proxy.ip}:{proxy.port}",
            proxy.extraction_method.url,
            protocol_name,
            proxy.last_check.strftime("%d/%m/%Y %H:%M:%S"),
        )
    print(table)
