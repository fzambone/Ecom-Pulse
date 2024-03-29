from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class CategoryResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    name: str
    price: float
    description: str
    quantity: int

class ProductCreate(ProductBase):
    category_id: int

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    int: int
    category: Optional[CategoryResponse] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
