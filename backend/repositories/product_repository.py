from sqlalchemy.orm import Session

from repositories.base_repository import BaseRepository
from repositories.models import Product

class ProductRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, Product)

    def find_available_products(self):
        return self.query().filter(Product.quantity > 0).all()