import factory
from faker import Faker
from faker.providers import DynamicProvider

from app.models import ExtractionMethod
from tests._factories.protocol import ProtocolFactory
from tests.database import Session

extraction_method_code_provider = DynamicProvider(
    provider_name="extraction_method_code",
    elements=["website_table_with_contry_code"],
)

fake = Faker()

# then add new provider to faker instance
fake.add_provider(extraction_method_code_provider)


class ExtractionMethodFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = ExtractionMethod
        sqlalchemy_session = Session
        sqlalchemy_session_persistence = "commit"

    id = factory.Faker("pyint", min_value=0, max_value=1000)
    name = factory.Faker("name")
    url = factory.Faker("url")
    priority = 0
    method = fake.extraction_method_code()

    protocol_id = factory.LazyAttribute(lambda obj: obj.protocol.id)
    protocol = factory.SubFactory(ProtocolFactory)
