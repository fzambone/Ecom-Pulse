from sqlalchemy.orm import Session

from backend.repositories.base_repository import BaseRepository
from backend.repositories.models import Category

class CategoryRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, Category)