from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from backend.schemas.visitor_schema import VisitorResponse

class EventBase(BaseModel):
    timestamp: datetime
    event_type: str
    page_url: str
    referrer: str
    product_id: Optional[int] = None

class EventCreate(EventBase):
    visitor_id: int

class EventUpdate(EventBase):
    pass

class EventResponse(EventBase):
    id: int
    visitor: VisitorResponse
    
    class Config:
        orm_mode = True