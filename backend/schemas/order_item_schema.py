from typing import Optional
from pydantic import BaseModel
from datetime import datetime

from backend.schemas.order_schema import OrderResponse
from backend.schemas.product_schema import ProductResponse

class OrderItemBase(BaseModel):
    orderid: int
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemUpdate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int
    order: OrderResponse
    product: ProductResponse

    class Config:
        orm_mode = True