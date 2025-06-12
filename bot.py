import asyncio
import logging
import json
import os

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode, ContentType
from aiogram.filters import CommandStart
from aiogram.types import (
    WebAppInfo,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder

logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

# Команда /start с Reply-кнопкой (обычная клавиатура)
@dp.message(CommandStart())
async def start(message: types.Message):
    webAppInfo = WebAppInfo(url="https://webapp-ox1d.onrender.com/")  # Твой вебапп
    builder = ReplyKeyboardBuilder()
    builder.add(KeyboardButton(text='Открыть WebApp', web_app=webAppInfo))
    await message.answer(text='Привет! Открой веб-приложение:', reply_markup=builder.as_markup(resize_keyboard=True))

# Обработка данных от WebApp
@dp.message(F.content_type == ContentType.WEB_APP_DATA)
async def parse_data(message: types.Message):
    data = json.loads(message.web_app_data.data)
    await message.answer(
        f'<b>{data["title"]}</b>\n\n<code>{data["desc"]}</code>\n\n{data["text"]}',
        parse_mode=ParseMode.HTML
    )

# Альтернативный старт с Inline-кнопкой (необязательно)
@dp.message(F.text.lower() == "inline")
async def send_inline(message: types.Message):
    web_app_url = "https://webapp-ox1d.onrender.com/"
    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton(
            text="Открыть WebApp",
            web_app=WebAppInfo(url=web_app_url)
        )
    )
    await message.answer("Нажми кнопку ниже, чтобы открыть WebApp:", reply_markup=keyboard)

# Главная функция
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
