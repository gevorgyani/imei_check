import httpx
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from core.db import get_async_session
from utils.validators import is_valid_imei
from services.imei_service import check_imei_with_api
from core.config import settings
from sqlalchemy.future import select
from models.imei_models import WhitelistUser
from whitelist_table.add_to_whitelist import add_to_whitelist


async def check_whitelist(telegram_id: int, session):
    result = await session.execute(select(WhitelistUser).where(WhitelistUser.telegram_id == telegram_id))
    return result.scalar() is not None


ADMIN_ID = 506849721  # Укажите свой Telegram ID


def create_bot():
    app = ApplicationBuilder().token(settings.BOT_TOKEN).build()

    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("Привет! Отправь IMEI для проверки.")

    async def check_imei_bot(update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = update.effective_user.id
        async for session in get_async_session():
            is_whitelisted = await check_whitelist(telegram_id, session)

        if not is_whitelisted:
            await update.message.reply_text("🚫 Доступ запрещен. Вас нет в белом списке.")
            return

        imei = update.message.text.strip()
        if not is_valid_imei(imei):
            await update.message.reply_text("❌ Неверный формат IMEI. Пожалуйста, попробуйте снова.")
            return

        try:
            api_response = await check_imei_with_api(imei)
            props = api_response.get("properties", {})
            device_name = props.get("deviceName", "Неизвестно")
            imei2 = props.get("imei2", "Нет данных")
            serial = props.get("serial", "Нет данных")
            region = props.get("apple/region", "Неизвестно")
            purchase_date = props.get("estPurchaseDate", "Нет данных")
            lost_mode = "✅ Нет" if not props.get("lostMode", False) else "❌ Да"
            refurbished = "✅ Нет" if not props.get("refurbished", False) else "❌ Да"

            response_text = (
                f"📱 **Данные устройства**:\n"
                f"🔹 **Модель:** {device_name}\n"
                f"🔹 **IMEI:** {imei}\n"
                f"🔹 **IMEI2:** {imei2}\n"
                f"🔹 **Серийный номер:** {serial}\n"
                f"🌍 **Регион:** {region}\n"
                f"📅 **Дата покупки:** {purchase_date}\n"
                f"🔄 **Восстановленный:** {refurbished}\n"
                f"🔍 **Режим утери:** {lost_mode}\n"
            )
            await update.message.reply_text(response_text, parse_mode="Markdown")
        except httpx.HTTPError:
            await update.message.reply_text("⚠ Не удалось получить данные из сервиса IMEI. Попробуйте позже.")

    async def add_whitelist(update: Update, context: ContextTypes.DEFAULT_TYPE):
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text("🚫 У вас нет прав на добавление пользователей в whitelist.")
            return

        if not context.args:
            await update.message.reply_text("⚠ Использование: `/add_whitelist <TELEGRAM_ID> <Имя>`", parse_mode="Markdown")
            return

        try:
            telegram_id = int(context.args[0])
            name = " ".join(context.args[1:]) if len(context.args) > 1 else "Неизвестный"

            async for session in get_async_session():
                added = await add_to_whitelist(telegram_id, name, session)

            if added:
                await update.message.reply_text(f"✅ Пользователь `{telegram_id}` добавлен в whitelist.")
            else:
                await update.message.reply_text(f"⚠ Пользователь `{telegram_id}` уже в whitelist.")

        except ValueError:
            await update.message.reply_text("❌ Ошибка: Telegram ID должен быть числом.")

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add_whitelist", add_whitelist))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, check_imei_bot))

    return app
