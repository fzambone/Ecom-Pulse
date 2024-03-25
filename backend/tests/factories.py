import factory
from factory.alchemy import SQLAlchemyModelFactory

from backend.repositories.models import Product
from backend.utils.database import SessionLocal

class ProductFactory(SQLAlchemyModelFactory):
    class Meta:
        model = Product
        sqlalchemy_session = SessionLocal
        sqlalchemy_session_persistence = 'commit'

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Sequence(lambda n: f"Test Product {n}")
    price = 10.0
    description = "Test Description"
    quantity = 50