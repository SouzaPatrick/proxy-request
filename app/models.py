from datetime import datetime
from typing import NoReturn, Optional

from sqlalchemy import desc
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.exc import NoResultFound
from sqlmodel import Column, Field, Relationship, Session, SQLModel, String, select


class BaseModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    @classmethod
    def exists(cls, session: Session, **kwargs) -> bool:
        if cls.get_by_fields(session=session, **kwargs) is not None:
            return True
        return False

    @classmethod
    def get_by_fields(cls, session, **kwargs):
        query = select(cls)

        for field, value in kwargs.items():
            field_name = getattr(cls, field)
            query = query.filter(field_name == value)
        try:
            result: Optional[cls] = session.execute(query).scalar()
            assert result is not None
        except (NoResultFound, AssertionError):
            result: Optional[cls] = None
        return result


class Protocol(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column("name", String, unique=True))

    extraction_method: list["ExtractionMethod"] = Relationship(
        back_populates="protocol"
    )

    def __str__(self):
        return f"<Protocol(name={self.name})>"

    def __repr__(self):
        return self.__str__()

    # Populate db install project
    @staticmethod
    def _populate_db(session: Session) -> list["Protocol"]:
        protocols: tuple[Protocol] = (
            Protocol(name="http"),
            Protocol(name="sock4"),
            Protocol(name="sock5"),
            Protocol(name="other"),
        )

        for protocol in protocols:
            session.add(protocol)
            session.commit()


class ExtractionMethod(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column("name", String, unique=True))
    url: str
    priority: int
    method: str

    proxy: list["Proxy"] = Relationship(back_populates="extraction_method")

    protocol_id: Optional[int] = Field(default=None, foreign_key="protocol.id")
    protocol: Optional[Protocol] = Relationship(back_populates="extraction_method")

    def __str__(self):
        return f"<ExtractionMethod(name={self.name})>"

    def __repr__(self):
        return self.__str__()

    # Populate db install project
    @staticmethod
    def _populate_db(session: Session) -> NoReturn:
        protocol_http_id: int = Protocol.get_by_fields(session=session, name="http").id

        extraction_methods: list[ExtractionMethod] = (
            ExtractionMethod(
                name="sslproxies",
                url="https://www.sslproxies.org",
                protocol_id=protocol_http_id,
                priority=0,
                method="website_table_with_contry_code",
            ),
            ExtractionMethod(
                name="freeproxy",
                url="https://free-proxy-list.net/",
                protocol_id=protocol_http_id,
                priority=0,
                method="website_table_with_contry_code",
            ),
        )

        for extraction_method in extraction_methods:
            session.add(extraction_method)
            session.commit()

    @staticmethod
    def get_all_extraction_methods_sorted_by_priority(
        session: Session,
    ) -> list["ExtractionMethod"]:
        query = select(ExtractionMethod).order_by(ExtractionMethod.priority)

        result: list[ExtractionMethod] = session.execute(query).scalars().all()

        return result


class Proxy(BaseModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ip: str
    port: int
    status_check: bool = Field(default=False)
    ttl: int  # Minutes
    last_check: datetime

    extraction_method_id: Optional[int] = Field(
        default=None, foreign_key="extractionmethod.id"
    )
    extraction_method: Optional[ExtractionMethod] = Relationship(back_populates="proxy")

    def __str__(self):
        return f"<Proxy(ip={self.ip}, port={self.port})>"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def get_all_valid_proxies(session: Session):
        query = (
            select(Proxy)
            .where(Proxy.status_check == True)  # noqa: E712
            .options(joinedload("extraction_method"))
            .order_by(desc(Proxy.last_check))
        )
        result: list[Proxy] = session.execute(query).scalars().all()

        return result

    def update_status(self, session: Session, status_check: bool = False) -> NoReturn:
        self.status_check = status_check
        self.last_check = datetime.now()

        session.add(self)
        session.commit()
