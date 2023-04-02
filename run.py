import sys

from app.commands import COMMANDS
from database import get_session


def command_run(command):
    with get_session() as session:
        command(session=session)


if len(sys.argv) == 2:
    command: str = sys.argv[1]

    match command:
        case "proxy":
            command_run(command=COMMANDS["proxy"])
        case "update":
            command_run(command=COMMANDS["update"])
        case "console":
            command_run(command=COMMANDS["console"])
        case other:
            raise NotImplementedError
else:
    raise NotImplementedError
