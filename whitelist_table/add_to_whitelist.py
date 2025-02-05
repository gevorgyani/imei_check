
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models.imei_models import WhitelistUser


async def add_to_whitelist(telegram_id: int, name: str, session: AsyncSession):
    result = await session.execute(select(WhitelistUser).where(WhitelistUser.telegram_id == telegram_id))
    user = result.scalar()

    if user:
        return False  # Уже в whitelist

    new_user = WhitelistUser(telegram_id=telegram_id, name=name)
    session.add(new_user)
    await session.commit()
    return True

