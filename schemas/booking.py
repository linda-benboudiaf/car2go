from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class BookingBase(BaseModel):
    user_id: int
    car_id: int
    start_time: datetime
    end_time: datetime
    purpose: str = Field(..., pattern="^(self|accompanied)$")

class BookingCreate(BookingBase):
    pass

class BookingUpdate(BaseModel):
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = Field(None, pattern="^(confirmée|annulée|terminée)$")
    purpose: Optional[str] = Field(None, pattern="^(self|accompanied)$")

class BookingResponse(BookingBase):
    id: int
    status: str
    purpose : str
    start_time : datetime
    end_time : datetime
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True