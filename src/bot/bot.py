import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from bot.handlers import handlers_router
from services.subscriptions_service import SubscriptionsService
from services.train_service import TrainService
from services.user_service import UserService


async def start_bot(user_service: UserService, train_service: TrainService, subscriptions_service: SubscriptionsService):
    # Initialize bot and dispatcher
    load_dotenv()
    api_token = os.getenv("API_TOKEN")
    if api_token is None:
        raise ValueError("API_TOKEN not found in .env file")
    bot = Bot(token=api_token)
    dp = Dispatcher()

    dp["user_service"] = user_service
    dp["train_service"] = train_service
    dp["subscriptions_service"] = subscriptions_service

    #registration routers
    dp.include_router(handlers_router)

    logging.info("Бот успешно запущен!")
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
