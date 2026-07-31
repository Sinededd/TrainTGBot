import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from bot.handlers import handlers_router


async def start_bot():
    # Configure logging
    logging.basicConfig(level=logging.INFO)

    # Initialize bot and dispatcher
    load_dotenv()
    api_token = os.getenv("API_TOKEN")
    if api_token is None:
        raise ValueError("API_TOKEN not found in .env file")
    bot = Bot(token=api_token)
    dp = Dispatcher()

    #registration routers
    dp.include_router(handlers_router)

    logging.info("Бот успешно запущен!")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
