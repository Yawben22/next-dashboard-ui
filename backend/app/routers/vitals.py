from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import get_db
from app.models.tables import Vital
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/vitals", tags=["vitals"]) 


class VitalCreate(BaseModel):
    patient_id: int
    recorded_at: Optional[datetime] = None
    temperature_c: Optional[float] = None
    pulse_bpm: Optional[int] = None
    systolic_bp: Optional[int] = None
    diastolic_bp: Optional[int] = None
    respiration_rate: Optional[int] = None


class VitalOut(BaseModel):
    id: int
    patient_id: int
    recorded_at: datetime
    temperature_c: Optional[float]
    pulse_bpm: Optional[int]
    systolic_bp: Optional[int]
    diastolic_bp: Optional[int]
    respiration_rate: Optional[int]

    class Config:
        from_attributes = True


@router.post("/", response_model=VitalOut)
async def create_vital(payload: VitalCreate, db: AsyncSession = Depends(get_db)):
    data = payload.model_dump()
    if data.get("recorded_at") is None:
        data["recorded_at"] = datetime.utcnow()
    obj = Vital(**data)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/", response_model=list[VitalOut])
async def list_vitals(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Vital))
    return list(result.scalars().all())
