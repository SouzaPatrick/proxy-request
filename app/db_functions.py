from datetime import datetime
from typing import NoReturn, Optional

from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound
from sqlmodel import Session, select

from app.database import get_engine
from app.models import ExtractionMethod, Protocol, Proxy


def get_valid_proxies() -> Optional[list[Proxy]]:
    query = (
        select(Proxy)
        .where(Proxy.status_check == True)
        .options(joinedload("extraction_method"))
        .order_by(desc(Proxy.last_check))
    )
    try:
        with Session(get_engine()) as session:
            result: Optional[list[Proxy]] = session.execute(query).scalars().all()
    except NoResultFound:
        result: Optional[list[Proxy]] = None

    return result


def get_protocol_with_id(protocol_id: int):
    query = select(Protocol).where(Protocol.id == protocol_id)
    try:
        with Session(get_engine()) as session:
            result = session.execute(query).scalar()
    except NoResultFound:
        result = None

    return result


def get_extract_methods() -> list[ExtractionMethod]:
    query = select(ExtractionMethod).order_by(ExtractionMethod.priority)

    with Session(get_engine()) as session:
        result: list[ExtractionMethod] = session.execute(query).scalars().all()

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


# Populate db
def populate_protocol() -> NoReturn:
    protocols: list[Protocol] = [
        Protocol(name="http"),
        Protocol(name="sock4"),
        Protocol(name="sock5"),
        Protocol(name="other"),
    ]

    with Session(get_engine()) as session:
        for protocol in protocols:
            session.add(protocol)
            session.commit()


def populate_extraction_method() -> NoReturn:
    extraction_methods: list[ExtractionMethod] = [
        ExtractionMethod(
            name="sslproxies",
            url="https://www.sslproxies.org",
            protocol_id=1,
            priority=0,
            method="website_table_with_contry_code",
        ),
        ExtractionMethod(
            name="freeproxy",
            url="https://free-proxy-list.net/",
            protocol_id=1,
            priority=0,
            method="website_table_with_contry_code",
        ),
    ]

    with Session(get_engine()) as session:
        for extraction_method in extraction_methods:
            session.add(extraction_method)
            session.commit()
