from typing import Optional
from pydantic import BaseModel


class RoomBase(BaseModel):
    number: str
    type: Optional[str] = None
    is_available: Optional[bool] = True


class RoomCreate(RoomBase):
    pass


class RoomUpdate(BaseModel):
    number: Optional[str] = None
    type: Optional[str] = None
    is_available: Optional[bool] = None


class RoomOut(RoomBase):
    id: int

    class Config:
        from_attributes = True
