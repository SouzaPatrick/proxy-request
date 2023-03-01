from datetime import datetime
from typing import List, Optional

from sqlmodel import Column, Field, Relationship, SQLModel, String


class Protocol(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str

    extraction_method: list["ExtractionMethod"] = Relationship(
        back_populates="protocol"
    )


class ExtractionMethod(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(sa_column=Column("name", String, unique=True))
    url: str
    priority: int
    method: str

    proxy: list["Proxy"] = Relationship(back_populates="extraction_method")

    protocol_id: Optional[int] = Field(default=None, foreign_key="protocol.id")
    protocol: Optional[Protocol] = Relationship(back_populates="extraction_method")


class Proxy(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    ip: str
    port: int
    status_check: bool = Field(default=False)
    ttl: int  # Minutes
    last_check: datetime

    extraction_method_id: Optional[int] = Field(
        default=None, foreign_key="extractionmethod.id"
    )
    extraction_method: Optional[ExtractionMethod] = Relationship(back_populates="proxy")
