import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

# === Твої дані ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
YOUR_CHANNEL_ID = os.getenv("CHANNEL_ID")
SOURCE = "sirena_dp"

# Текст для тривоги
ALERT_TEXT = """⚠️ <b>ПОВІТРЯНА ТРИВОГА!</b>
📍 Дніпро та Дніпропетровська область

"""

# Текст для відбою
ALL_CLEAR_TEXT = """✅ <b>ВІДБІЙ ТРИВОГИ</b>
📍 Дніпро та Дніпропетровська область

"""

# Новий правильний спосіб ініціалізації бота
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher()

@dp.message(F.forward_from_chat)
async def smart_alert(message: Message):
    if not (message.forward_from_chat and message.forward_from_chat.username == SOURCE):
        return

    original = message.text or message.caption or ""
    lower = original.lower()

    try:
        if any(word in lower for word in ["тривог", "сирена", "укриття", "повітряна"]):
            prefix = ALERT_TEXT
            print("⚠️ Виявлено ТРИВОГУ")
        elif any(word in lower for word in ["відбій", "відбою"]):
            prefix = ALL_CLEAR_TEXT
            print("✅ Виявлено ВІДБІЙ")
        else:
            return

        await message.copy_to(
            chat_id=YOUR_CHANNEL_ID,
            caption=prefix + original
        )
        print("✅ Повідомлення надіслано в канал")
    except Exception as e:
        print(f"Помилка: {e}")

async def main():
    print("🚀 Бот повітряної тривоги по Дніпру запущений!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
