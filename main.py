import threading
import asyncio
from fastapi import FastAPI
from routers.api import app as fastapi_app
from routers.bot import create_bot

bot_app = create_bot()

def run_telegram_bot():
    # Создаем новый событийный цикл
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(bot_app.run_polling())

# Запускаем Telegram-бота в отдельном потоке
telegram_thread = threading.Thread(target=run_telegram_bot, daemon=True)
telegram_thread.start()

# FastAPI приложение
app = fastapi_app
