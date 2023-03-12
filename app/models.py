from datetime import datetime
from typing import Optional

from sqlalchemy.orm.exc import NoResultFound
from sqlmodel import Column, Field, Relationship, Session, SQLModel, String, select

from app.database import get_engine


class BaseModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)

    @classmethod
    def exists(cls, **kwargs) -> bool:
        if cls.get_by_fields(**kwargs) is not None:
            return True
        return False

    @classmethod
    def get_by_fields(cls, **kwargs):
        query = select(cls)

        for field, value in kwargs.items():
            field_name = getattr(cls, field)
            query = query.filter(field_name == value)
        try:
            with Session(get_engine()) as session:
                result: Optional[cls] = session.execute(query).one()
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
