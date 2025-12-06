from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# What the user sends to create an alert
class AlertCreate(BaseModel):
    city: str
    temperature_min: Optional[float] = None
    temperature_max: Optional[float] = None
    condition: Optional[str] = None # e.g. "Rain"
    user_email: str

# What we return to the user (includes the ID and created_at)
class AlertResponse(AlertCreate):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True # Tells Pydantic to read from SQLAlchemy models

# What a Log entry looks like
class LogResponse(BaseModel):
    city: str
    message: str
    triggered_at: datetime

    class Config:
        orm_mode = True