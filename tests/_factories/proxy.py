from datetime import datetime

import factory
from faker import Faker

from app.models import Proxy
from settings import TTL_PROXY
from tests._factories.extract_method import ExtractionMethodFactory
from tests.database import Session

fake = Faker()


class ProxyFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Proxy
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"

    id = factory.Faker("pyint", min_value=0, max_value=1000)
    ip = fake.ipv4_public()
    port = fake.port_number()
    status_check = True
    ttl = TTL_PROXY
    last_check = datetime.now()

    extraction_method_id = factory.LazyAttribute(lambda obj: obj.extraction_method.id)
    extraction_method = factory.SubFactory(ExtractionMethodFactory)
