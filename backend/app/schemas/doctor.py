from typing import Optional
from pydantic import BaseModel


class DoctorBase(BaseModel):
    user_id: int
    department_id: Optional[int] = None
    specialization: Optional[str] = None


class DoctorCreate(DoctorBase):
    pass


class DoctorUpdate(BaseModel):
    department_id: Optional[int] = None
    specialization: Optional[str] = None


class DoctorOut(DoctorBase):
    id: int

    class Config:
        from_attributes = True
