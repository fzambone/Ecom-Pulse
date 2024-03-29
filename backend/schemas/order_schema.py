from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from backend.schemas.order_item_schema import OrderItemResponse
from backend.schemas.visitor_schema import VisitorResponse

class OrderBase(BaseModel):
    timestamp: datetime
    total_amount: float

class OrderCreate(OrderBase):
    visitor_id: int

class OrderUpdate(OrderBase):
    pass

class OrderResponse(OrderBase):
    id: int
    visitor: VisitorResponse
    order_items: List[OrderItemResponse] = []