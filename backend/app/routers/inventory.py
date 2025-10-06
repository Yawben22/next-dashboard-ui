from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import get_db
from app.models.tables import InventoryItem
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/inventory", tags=["inventory"]) 


class InventoryItemCreate(BaseModel):
    name: str
    sku: Optional[str] = None
    quantity: int
    unit: Optional[str] = None


class InventoryItemUpdate(BaseModel):
    name: Optional[str] = None
    sku: Optional[str] = None
    quantity: Optional[int] = None
    unit: Optional[str] = None


class InventoryItemOut(BaseModel):
    id: int
    name: str
    sku: Optional[str]
    quantity: int
    unit: Optional[str]

    class Config:
        from_attributes = True


@router.post("/items", response_model=InventoryItemOut)
async def create_item(payload: InventoryItemCreate, db: AsyncSession = Depends(get_db)):
    item = InventoryItem(**payload.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.get("/items", response_model=list[InventoryItemOut])
async def list_items(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(InventoryItem))
    return list(result.scalars().all())


@router.patch("/items/{item_id}", response_model=InventoryItemOut)
async def update_item(item_id: int, payload: InventoryItemUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(InventoryItem).where(InventoryItem.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    for k, v in payload.model_dump(exclude_unset=True).items():
        setattr(item, k, v)
    await db.commit()
    await db.refresh(item)
    return item
