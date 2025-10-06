from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import get_db
from app.models.tables import MedicalRecord
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/medical-records", tags=["medical_records"]) 


class MedicalRecordCreate(BaseModel):
    patient_id: int
    doctor_id: Optional[int] = None
    visit_date: Optional[datetime] = None
    diagnosis: Optional[str] = None
    treatment: Optional[str] = None


class MedicalRecordOut(BaseModel):
    id: int
    patient_id: int
    doctor_id: Optional[int]
    visit_date: datetime
    diagnosis: Optional[str]
    treatment: Optional[str]

    class Config:
        from_attributes = True


@router.post("/", response_model=MedicalRecordOut)
async def create_medical_record(payload: MedicalRecordCreate, db: AsyncSession = Depends(get_db)):
    data = payload.model_dump()
    if data.get("visit_date") is None:
        data["visit_date"] = datetime.utcnow()
    obj = MedicalRecord(**data)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/", response_model=list[MedicalRecordOut])
async def list_medical_records(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MedicalRecord))
    return list(result.scalars().all())
