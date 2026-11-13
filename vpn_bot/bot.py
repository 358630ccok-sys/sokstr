import asyncio
import logging
import os
import sqlite3
from datetime import datetime

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
DB_PATH = os.getenv("DB_PATH", "vpn_sales.db")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    handlers=[logging.StreamHandler(), logging.FileHandler("bot.log")],
)
logger = logging.getLogger(__name__)


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS clients (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            created_at TEXT,
            status TEXT
        )
        """
    )
    conn.commit()
    conn.close()


def add_client(user_id: int, username: str | None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT OR REPLACE INTO clients (user_id, username, created_at, status) VALUES (?, ?, ?, ?)",
        (user_id, username or "", datetime.utcnow().isoformat(), "active"),
    )
    conn.commit()
    conn.close()
    logger.info("client saved: user_id=%s username=%s", user_id, username)


dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    kb = InlineKeyboardBuilder()
    kb.button(text="Купить VPN (100 руб)", callback_data="buy")
    await message.answer("Привет! Добро пожаловать в VPN-сервис.", reply_markup=kb.as_markup())


@dp.callback_query(F.data == "buy")
async def cb_buy(callback: types.CallbackQuery):
    user = callback.from_user
    add_client(user.id, user.username)
    await callback.message.answer("vless://test-link")
    await callback.answer("Ссылка сгенерирована")


@dp.message(Command("status"))
async def cmd_status(message: types.Message):
    await message.answer("Трафик: 0 ГБ / без ограничений")


async def main():
    if not BOT_TOKEN:
        logger.warning("BOT_TOKEN is not set (using placeholder)")
    init_db()
    bot = Bot(token=BOT_TOKEN or "PLACEHOLDER_TOKEN")
    logger.info("bot starting")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
