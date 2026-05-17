import asyncio
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from dotenv import load_dotenv

load_dotenv()

# === Твої дані ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
YOUR_CHANNEL_ID = os.getenv("CHANNEL_ID")
SOURCE = "sirena_dp"

# Текст для тривоги
ALERT_TEXT = """⚠️ <b>Увага! Повітряна тривога!</b>
📍 Дніпро та Дніпропетровська область

"""

# Текст для відбою
ALL_CLEAR_TEXT = """✅ <b>Відбій повітряної тривоги.</b>
📍 Дніпро та Дніпропетровська область

"""

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
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
            print("⚠️ Увага! Повітряна тривога!")
        elif any(word in lower for word in ["відбій", "відбою"]):
            prefix = ALL_CLEAR_TEXT
            print("✅ "Відбій повітряної тривоги.")
        else:
            return

        await message.copy_to(
            chat_id=YOUR_CHANNEL_ID,
            caption=prefix + original,
            parse_mode="HTML"
        )
        print("✅ Повідомлення успішно надіслано в канал")
    except Exception as e:
        print(f"Помилка: {e}")

async def main():
    print("🚀 Бот повітряної тривоги по Дніпру успішно запущений!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
