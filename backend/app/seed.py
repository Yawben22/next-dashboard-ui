import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import SessionLocal
from app.models.tables import Department, Room


async def seed():
    async with SessionLocal() as db:  # type: AsyncSession
        # Departments
        existing = await db.execute(select(Department))
        if not existing.scalars().first():
            db.add_all([
                Department(name="Cardiology", description="Heart"),
                Department(name="Neurology", description="Brain"),
                Department(name="Emergency", description="Emergency"),
            ])

        # Rooms
        r = await db.execute(select(Room))
        if not r.scalars().first():
            db.add_all([
                Room(number="101", type="ICU"),
                Room(number="102", type="Private"),
                Room(number="201", type="General"),
            ])

        await db.commit()


if __name__ == "__main__":
    asyncio.run(seed())
