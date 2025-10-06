from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.db import init_db
from app.routers import health

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

@app.get("/")
async def root():
    return {"status": "ok", "service": "hms"}
