from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import get_db
from app.schemas.doctor import DoctorCreate, DoctorUpdate, DoctorOut
from app.models.tables import Doctor

router = APIRouter(prefix="/doctors", tags=["doctors"]) 


@router.post("/", response_model=DoctorOut)
async def create_doctor(payload: DoctorCreate, db: AsyncSession = Depends(get_db)):
    doc = Doctor(**payload.model_dump())
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc


@router.get("/", response_model=list[DoctorOut])
async def list_doctors(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Doctor))
    return list(result.scalars().all())


@router.get("/{doctor_id}", response_model=DoctorOut)
async def get_doctor(doctor_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doc


@router.patch("/{doctor_id}", response_model=DoctorOut)
async def update_doctor(doctor_id: int, payload: DoctorUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Doctor).where(Doctor.id == doctor_id))
    doc = result.scalar_one_or_none()
    if not doc:
        raise HTTPException(status_code=404, detail="Doctor not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(doc, k, v)
    await db.commit()
    await db.refresh(doc)
    return doc
