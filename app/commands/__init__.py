from app.commands.console import console
from app.commands.proxy import proxy
from app.commands.update import update_proxy_status

COMMANDS = {"proxy": proxy, "update": update_proxy_status, "console": console}
