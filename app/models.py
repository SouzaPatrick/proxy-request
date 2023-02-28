from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Proxy(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now, nullable=False)
    ip: str
    port: int
    status_check: bool = Field(default=False)
    ttl: int  # Minutes
    last_check: datetime
