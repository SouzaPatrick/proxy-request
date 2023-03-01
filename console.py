from typing import Optional

from rich import box, print
from rich.table import Table

from app.db_functions import get_valid_proxies, get_protocol_with_id
from app.models import Proxy

table = Table(title="Table of valid proxies", box=box.SIMPLE)
table.add_column("Nº")
table.add_column("PROXY")
table.add_column("Url")
table.add_column("Protocol")
table.add_column("Last check")

proxies: Optional[list[Proxy]] = get_valid_proxies()
for index, proxy in enumerate(proxies):
    table.add_row(
        str(index),
        f"{proxy.ip}:{proxy.port}",
        proxy.extraction_method.url,
        get_protocol_with_id(proxy.extraction_method.protocol_id).name,
        proxy.last_check.strftime("%d/%m/%Y %H:%M:%S"),
    )
print(table)
