from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import get_db
from app.models.tables import LabTest
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/lab-tests", tags=["lab_tests"]) 


class LabTestCreate(BaseModel):
    patient_id: int
    ordered_by_doctor_id: int
    test_name: str
    result: Optional[str] = None
    status: Optional[str] = "ordered"


class LabTestUpdate(BaseModel):
    result: Optional[str] = None
    status: Optional[str] = None


class LabTestOut(BaseModel):
    id: int
    patient_id: int
    ordered_by_doctor_id: int
    test_name: str
    result: Optional[str]
    status: str

    class Config:
        from_attributes = True


@router.post("/", response_model=LabTestOut)
async def create_lab_test(payload: LabTestCreate, db: AsyncSession = Depends(get_db)):
    obj = LabTest(**payload.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj


@router.get("/", response_model=list[LabTestOut])
async def list_lab_tests(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(LabTest))
    return list(result.scalars().all())


@router.patch("/{lab_test_id}", response_model=LabTestOut)
async def update_lab_test(lab_test_id: int, payload: LabTestUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(LabTest).where(LabTest.id == lab_test_id))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Lab test not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    await db.commit()
    await db.refresh(obj)
    return obj
