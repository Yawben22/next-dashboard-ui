from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import get_db
from app.models.tables import Admission
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/admissions", tags=["admissions"]) 


class AdmissionCreate(BaseModel):
    patient_id: int
    room_id: Optional[int] = None
    admitted_at: Optional[datetime] = None
    reason: Optional[str] = None


class AdmissionUpdate(BaseModel):
    room_id: Optional[int] = None
    discharged_at: Optional[datetime] = None
    reason: Optional[str] = None


class AdmissionOut(BaseModel):
    id: int
    patient_id: int
    room_id: Optional[int]
    admitted_at: datetime
    discharged_at: Optional[datetime]
    reason: Optional[str]

    class Config:
        from_attributes = True


@router.post("/", response_model=AdmissionOut)
async def create_admission(payload: AdmissionCreate, db: AsyncSession = Depends(get_db)):
    data = payload.model_dump()
    if data.get("admitted_at") is None:
        data["admitted_at"] = datetime.utcnow()
    adm = Admission(**data)
    db.add(adm)
    await db.commit()
    await db.refresh(adm)
    return adm


@router.get("/", response_model=list[AdmissionOut])
async def list_admissions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Admission))
    return list(result.scalars().all())


@router.patch("/{admission_id}", response_model=AdmissionOut)
async def update_admission(admission_id: int, payload: AdmissionUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Admission).where(Admission.id == admission_id))
    adm = result.scalar_one_or_none()
    if not adm:
        raise HTTPException(status_code=404, detail="Admission not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(adm, k, v)
    await db.commit()
    await db.refresh(adm)
    return adm
