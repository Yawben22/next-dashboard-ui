from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import get_db
from app.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentOut
from app.models.tables import Appointment

router = APIRouter(prefix="/appointments", tags=["appointments"]) 


@router.post("/", response_model=AppointmentOut)
async def create_appointment(payload: AppointmentCreate, db: AsyncSession = Depends(get_db)):
    appointment = Appointment(**payload.model_dump())
    db.add(appointment)
    await db.commit()
    await db.refresh(appointment)
    return appointment


@router.get("/", response_model=list[AppointmentOut])
async def list_appointments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Appointment))
    return list(result.scalars().all())


@router.get("/{appointment_id}", response_model=AppointmentOut)
async def get_appointment(appointment_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Appointment).where(Appointment.id == appointment_id))
    appointment = result.scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


@router.patch("/{appointment_id}", response_model=AppointmentOut)
async def update_appointment(appointment_id: int, payload: AppointmentUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Appointment).where(Appointment.id == appointment_id))
    appointment = result.scalar_one_or_none()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(appointment, k, v)
    await db.commit()
    await db.refresh(appointment)
    return appointment
