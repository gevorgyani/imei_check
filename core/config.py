from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite+aiosqlite:///./whitelist.db"
    IMEI_API_URL: str = "https://api.imeicheck.net"
    IMEI_API_TOKEN: str = "e4oEaZY1Kom5OXzybETkMlwjOCy3i8GSCGTHzWrhd4dc563b"
    BOT_TOKEN: str
    API_AUTH_TOKEN: str

    class Config:
        env_file = ".env"

settings = Settings()
