from rich import print, box
from rich.table import Table
from app.db_functions import get_valid_proxies

from typing import Optional
from app.models import Proxy
table = Table(
    title='Table of valid proxies',
    box=box.SIMPLE
)
table.add_column(
    "Nº"
)
table.add_column(
    "PROXY"
)
table.add_column(
    "TTL (minutes)"
)
table.add_column(
    "Last check"
)
proxies: Optional[list[Proxy]] = get_valid_proxies()
for index, proxy in enumerate(proxies):
    table.add_row(str(index), f"{proxy.ip}:{proxy.port}", str(proxy.ttl), proxy.last_check.strftime("%d/%m/%Y %H:%M:%S"))

print(table)
