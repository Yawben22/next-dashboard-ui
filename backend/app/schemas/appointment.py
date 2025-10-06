from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    scheduled_for: datetime
    status: Optional[str] = "scheduled"
    notes: Optional[str] = None


class AppointmentCreate(AppointmentBase):
    pass


class AppointmentUpdate(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    scheduled_for: Optional[datetime] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class AppointmentOut(AppointmentBase):
    id: int

    class Config:
        from_attributes = True
