
from sqlalchemy.orm import Session

from backend.repositories.base_repository import BaseRepository
from backend.repositories.models import Visitor


class VisitorRepository(BaseRepository):
    def __init__(self, db: Session):
        super().__init__(db, Visitor)

    def find_by_location(self, location: str):
        return self.db.query(Visitor).filter(Visitor.approximate_location == location).all()