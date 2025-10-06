from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import get_db
from app.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentOut
from app.models.tables import Department

router = APIRouter(prefix="/departments", tags=["departments"]) 


@router.post("/", response_model=DepartmentOut)
async def create_department(payload: DepartmentCreate, db: AsyncSession = Depends(get_db)):
    dept = Department(**payload.model_dump())
    db.add(dept)
    await db.commit()
    await db.refresh(dept)
    return dept


@router.get("/", response_model=list[DepartmentOut])
async def list_departments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Department))
    return list(result.scalars().all())


@router.get("/{department_id}", response_model=DepartmentOut)
async def get_department(department_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Department).where(Department.id == department_id))
    dept = result.scalar_one_or_none()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    return dept


@router.patch("/{department_id}", response_model=DepartmentOut)
async def update_department(department_id: int, payload: DepartmentUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Department).where(Department.id == department_id))
    dept = result.scalar_one_or_none()
    if not dept:
        raise HTTPException(status_code=404, detail="Department not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(dept, k, v)
    await db.commit()
    await db.refresh(dept)
    return dept
