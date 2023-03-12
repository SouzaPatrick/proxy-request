from typing import Optional

from app.db_functions import get_protocol_with_id
from app.models import Protocol
from tests._factories import ProtocolFactory


def test_get_protocol_with_id(session):
    protocol: Protocol = ProtocolFactory()
    protocol_found: Optional[Protocol] = get_protocol_with_id(
        session=session, protocol_id=protocol.id
    )

    assert protocol.id == protocol_found.id
    assert protocol.name == protocol_found.name
