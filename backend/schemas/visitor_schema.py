from typing import Optional
from pydantic import BaseModel
from datetime import datetime

class VisitorBase(BaseModel):
    approximate_location: str
    session_start_time: datetime
    ip_address: str

class VisitorCreate(VisitorBase):
    pass

class VisitorUpdate(VisitorBase):
    pass

class VisitorResponse(VisitorBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class config:
        orm_mode = True