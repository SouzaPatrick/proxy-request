from typing import NoReturn, Optional

from sqlalchemy.orm.exc import NoResultFound
from sqlmodel import Session, select

from app.models import ExtractionMethod, Protocol, Proxy
from database import get_engine


def get_protocol_with_id(session: Session, protocol_id: int) -> Optional[Protocol]:
    query = select(Protocol).where(Protocol.id == protocol_id)
    try:
        result: Optional[Protocol] = session.execute(query).scalar()
    except NoResultFound:
        result = None

    return result


def get_extract_methods() -> list[ExtractionMethod]:
    query = select(ExtractionMethod).order_by(ExtractionMethod.priority)

    with Session(get_engine()) as session:
        result: list[ExtractionMethod] = session.execute(query).scalars().all()

    return result


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
