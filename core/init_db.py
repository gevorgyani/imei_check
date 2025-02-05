import asyncio
from db import engine, Base

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all) #Использует метаданные из базового класса Base,
        # чтобы создать таблицы в базе данных на основе определённых моделей (WhitelistUser)

if __name__ == "__main__":
    asyncio.run(init_models())
