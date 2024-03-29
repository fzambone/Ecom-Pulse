from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

from backend.schemas.product_schema import ProductResponse


class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    products: List[ProductResponse] = []

    class Config:
        orm_mode = True