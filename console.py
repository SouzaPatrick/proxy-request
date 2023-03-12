from typing import Optional

from rich import box, print
from rich.table import Table

from app.db_functions import get_protocol_with_id
from app.models import Proxy
from database import get_session

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
        protocol_name: str = get_protocol_with_id(
            session=session, protocol_id=proxy.extraction_method.protocol_id
        ).name
    table.add_row(
        str(index),
        f"{proxy.ip}:{proxy.port}",
        proxy.extraction_method.url,
        protocol_name,
        proxy.last_check.strftime("%d/%m/%Y %H:%M:%S"),
    )
print(table)
