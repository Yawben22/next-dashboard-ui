from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.db import init_db
from app.routers import health
from app.routers import auth, patients, departments, rooms, doctors, appointments
from app.routers import admissions, prescriptions, lab_tests, vitals, medical_records, billing, inventory

app = FastAPI(title="Hospital Management System", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def on_startup() -> None:
    await init_db()

app.include_router(health.router, prefix="/api")
app.include_router(auth.router, prefix="/api")
app.include_router(patients.router, prefix="/api")
app.include_router(departments.router, prefix="/api")
app.include_router(rooms.router, prefix="/api")
app.include_router(doctors.router, prefix="/api")
app.include_router(appointments.router, prefix="/api")
app.include_router(admissions.router, prefix="/api")
app.include_router(prescriptions.router, prefix="/api")
app.include_router(lab_tests.router, prefix="/api")
app.include_router(vitals.router, prefix="/api")
app.include_router(medical_records.router, prefix="/api")
app.include_router(billing.router, prefix="/api")
app.include_router(inventory.router, prefix="/api")

@app.get("/")
async def root():
    return {"status": "ok", "service": "hms"}
