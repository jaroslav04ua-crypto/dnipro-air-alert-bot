import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

# ================== НАЛАШТУВАННЯ ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")
YOUR_CHANNEL_ID = os.getenv("CHANNEL_ID")
SOURCE_USERNAME = "sirena_dp"          # офіційний канал Дніпра

# Твій текст, який буде додаватися перед повідомленням
CUSTOM_TEXT = "⚠️ Повітряна тривога по Дніпру та області\n\n"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(F.forward_from_chat)
async def copy_alert(message: Message):
    if message.forward_from_chat and message.forward_from_chat.username == SOURCE_USERNAME:
        try:
            # Копіюємо повідомлення БЕЗ відмітки "переслано"
            await message.copy_to(
                chat_id=YOUR_CHANNEL_ID,
                caption=CUSTOM_TEXT + (message.caption or message.text or ""),
                parse_mode="HTML"
            )
            print(f"✅ Скопійовано повідомлення з @{SOURCE_USERNAME}")
        except Exception as e:
            print(f"Помилка: {e}")

async def main():
    print("🚀 Бот запущений! Копіює тривоги з @sirena_dp з твоїм текстом")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
