from sqlalchemy import Column, Integer, String
from core.db import Base

class WhitelistUser(Base):
    __tablename__ = "whitelist_users"

    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, index=True)
    name = Column(String, nullable=True)
