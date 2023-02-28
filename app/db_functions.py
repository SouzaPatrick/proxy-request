from datetime import datetime
from typing import NoReturn, Optional

from sqlalchemy import desc
from sqlalchemy.orm.exc import NoResultFound
from sqlmodel import Session, select

from app.database import get_engine
from app.models import Proxy


def get_valid_proxies() -> Optional[list[Proxy]]:
    query = (
        select(Proxy).where(Proxy.status_check == True).order_by(desc(Proxy.last_check))
    )
    try:
        with Session(get_engine()) as session:
            result: Optional[list[Proxy]] = session.execute(query).scalars().all()
    except NoResultFound:
        result: Optional[list[Proxy]] = None

    return result


def exist_proxy(ip: str, port: int) -> bool:
    query = select(Proxy).where(Proxy.ip == ip, Proxy.port == port)

    with Session(get_engine()) as session:
        result = session.execute(query).scalars().first()

    if result:
        return True
    return False


def update_status_check_proxy(
    proxy: Proxy, status_check: bool = False, last_check: datetime = datetime.now()
) -> NoReturn:
    with Session(get_engine()) as session:
        proxy.status_check = status_check
        proxy.last_check = last_check

        session.add(proxy)
        session.commit()


def create_proxies(proxies: list[Proxy]) -> NoReturn:
    with Session(get_engine()) as session:
        for proxy in proxies:
            session.add(proxy)
            session.commit()


def populate_db() -> NoReturn:
    proxies: list[Proxy] = [
        Proxy(
            ip="158.255.212.55",
            port=3256,
            status_check=True,
            ttl=30,
            last_check=datetime.now(),
        ),
        Proxy(
            ip="45.116.156.235",
            port=8080,
            status_check=True,
            ttl=30,
            last_check=datetime.now(),
        ),
    ]

    with Session(get_engine()) as session:
        for proxy in proxies:
            session.add(proxy)
            session.commit()
