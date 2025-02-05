from sqlalchemy import Column, Integer
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import declarative_base, sessionmaker, declared_attr
from core.config import settings  # Импорт настроек

# Базовый класс для моделей
class PreBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id = Column(Integer, primary_key=True)

Base = declarative_base(cls=PreBase)

# Создание движка и сессий
engine = create_async_engine(settings.DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession,
    autocommit=False, #Транзакции не будут автоматически коммититься.
    autoflush=False, #Изменения в объектах не будут автоматически записываться в базу
    expire_on_commit=False) #Отключает автоматическую аннулирование объектов после коммита.

# Асинхронная функция для получения сессии
async def get_async_session():
    async with AsyncSessionLocal() as async_session:
        yield async_session
