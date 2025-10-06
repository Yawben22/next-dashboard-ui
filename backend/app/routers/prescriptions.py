from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import get_db
from app.models.tables import Prescription
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/prescriptions", tags=["prescriptions"]) 


class PrescriptionCreate(BaseModel):
    patient_id: int
    doctor_id: int
    medication_name: str
    dosage: str
    frequency: str
    duration_days: int


class PrescriptionUpdate(BaseModel):
    medication_name: Optional[str] = None
    dosage: Optional[str] = None
    frequency: Optional[str] = None
    duration_days: Optional[int] = None


class PrescriptionOut(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    medication_name: str
    dosage: str
    frequency: str
    duration_days: int

    class Config:
        from_attributes = True


@router.post("/", response_model=PrescriptionOut)
async def create_prescription(payload: PrescriptionCreate, db: AsyncSession = Depends(get_db)):
    obj = Prescription(**payload.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/", response_model=list[PrescriptionOut])
async def list_prescriptions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Prescription))
    return list(result.scalars().all())


@router.patch("/{prescription_id}", response_model=PrescriptionOut)
async def update_prescription(prescription_id: int, payload: PrescriptionUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Prescription).where(Prescription.id == prescription_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Prescription not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj
