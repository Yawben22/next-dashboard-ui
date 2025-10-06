from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import get_db
from app.models.tables import Invoice, InvoiceItem, Payment
from pydantic import BaseModel
from typing import Optional, List

router = APIRouter(prefix="/billing", tags=["billing"]) 


class InvoiceCreate(BaseModel):
    patient_id: int


class InvoiceItemCreate(BaseModel):
    description: str
    amount: float


class PaymentCreate(BaseModel):
    amount: float
    method: str


class InvoiceOut(BaseModel):
    id: int
    patient_id: int
    status: str
    total_amount: float

    class Config:
        from_attributes = True


@router.post("/invoices", response_model=InvoiceOut)
async def create_invoice(payload: InvoiceCreate, db: AsyncSession = Depends(get_db)):
    invoice = Invoice(patient_id=payload.patient_id, total_amount=0.0, status="unpaid")
    db.add(invoice)
    await db.commit()
    await db.refresh(invoice)
    return invoice


@router.post("/invoices/{invoice_id}/items", response_model=InvoiceOut)
async def add_invoice_item(invoice_id: int, payload: InvoiceItemCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id))
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    item = InvoiceItem(invoice_id=invoice_id, description=payload.description, amount=payload.amount)
    db.add(item)
    invoice.total_amount += payload.amount
    await db.commit()
    await db.refresh(invoice)
    return invoice


@router.post("/invoices/{invoice_id}/payments", response_model=InvoiceOut)
async def add_payment(invoice_id: int, payload: PaymentCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id))
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    payment = Payment(invoice_id=invoice_id, amount=payload.amount, method=payload.method)
    db.add(payment)
    # simplistic: mark paid when total covered
    if payload.amount >= invoice.total_amount:
        invoice.status = "paid"
    await db.commit()
    await db.refresh(invoice)
    return invoice
