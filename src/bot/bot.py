import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from playwright.async_api import Playwright

from bot.handlers import handlers_router
from bot.notifier import TelegramNotifier
from repository.train_repository import TrainRepository
from services.booking_service import BookingService
from services.subscription_monitor import SubscriptionMonitorService
from services.subscriptions_service import SubscriptionsService
from services.train_service import TrainService
from services.user_service import UserService


async def start_bot(playwright: Playwright, user_service: UserService, train_service: TrainService,
                    subscriptions_service: SubscriptionsService, train_repository: TrainRepository):
    # Initialize bot and dispatcher
    load_dotenv()
    api_token = os.getenv("TELEGRAM_BOT_TOKEN")
    if api_token is None:
        raise ValueError("TELEGRAM_BOT_TOKEN not found in .env file")
    bot = Bot(token=api_token)
    dp = Dispatcher()

    dp["user_service"] = user_service
    dp["train_service"] = train_service
    dp["subscriptions_service"] = subscriptions_service

    browser = await playwright.chromium.launch(headless=True, slow_mo=250)

    booking_service = BookingService(
        train_repository=train_repository,
        user_service=user_service,
        browser=browser,
    )

    notifier = TelegramNotifier(bot=bot)
    monitor_service = SubscriptionMonitorService(
        subscriptions_repo=subscriptions_service.subscriptions_repo,
        train_service=train_service,
        booking_service=booking_service,
        notifier=notifier,
        request_delay_seconds=5.0,
        check_interval_seconds=600
    )

    monitor_task = asyncio.create_task(monitor_service.start())

    # registration routers
    dp.include_router(handlers_router)

    logging.info("Bot successfully started!")
    try:
        await dp.start_polling(bot)
    finally:
        monitor_service.stop()
        monitor_task.cancel()
        try:
            await monitor_task
        except asyncio.CancelledError:
            pass
        try:
            await browser.close()
        except Exception:
            pass
        await bot.session.close()
