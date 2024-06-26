from datetime import datetime
import random
from typing import Type, TypeVar
from sqlalchemy import delete, null, update
from sqlalchemy.orm import Session, Query

from utils.database import Base

T = TypeVar('T', bound=Base)

class BaseRepository:
    def __init__(self, db: Session, model: Type[T]):
        self.db = db
        self.model = model

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.db.query(self.model).filter(self.model.deleted_at == None).offset(skip).limit(limit)
    
    def get(self, id):
        return self.db.query(self.model).filter(self.model.id == id, self.model.deleted_at == None).first()
    
    def create(self, entity):
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def update(self, entity):
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity
    
    def soft_delete(self, id):
        update_stmt = (
            update(self.model).where(self.model.id == id).values(deleted_at=datetime.now())
        )
        self.db.execute(update_stmt)
        self.db.commit()

    def restore(self, id):
        update_stmt = (
            update(self.model).where(self.model.id == id).values(deleted_at=None)
        )
        self.db.execute(update_stmt)
        self.db.commit()

    def list_deleted(self):
        return self.db.query(self.model).filter(self.model.deleted_at is not None).all()
    
    def query(self) -> Query:
        return self.db.query(self.model).filter(self.model.deleted_at == None)
    
    def hard_delete(self, id):
        delete_stmt = delete(self.model).where(self.model.id == id)
        self.db.execute(delete_stmt)
        self.db.commit()

    def get_random_id(self, entity):
        ids = self.db.query(entity.id).all()
        if not ids:
            return None
        return random.choice(ids)[0]