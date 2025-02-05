import asyncio
from core.db import engine, Base
from models.imei_models import WhitelistUser

async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Таблицы успешно созданы!")

if __name__ == "__main__":
    asyncio.run(create_tables())