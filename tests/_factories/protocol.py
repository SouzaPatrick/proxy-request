import factory
from faker import Faker
from faker.providers import DynamicProvider

from app.models import Protocol
from tests.database import Session

protocol_name_provider = DynamicProvider(
    provider_name="protocol_name",
    elements=["http", "sock4", "sock5", "other"],
)

fake = Faker()

# then add new provider to faker instance
fake.add_provider(protocol_name_provider)


class ProtocolFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Protocol
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"

    id = factory.Faker("pyint", min_value=0, max_value=1000)
    name = fake.protocol_name()
