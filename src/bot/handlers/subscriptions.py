from venv import logger

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.handlers.train_views import send_trains
from services.subscriptions_service import SubscriptionsService

router = Router()

@router.message(Command("subscriptions"))
async def command_subscriptions(message: Message, subscriptions_service: SubscriptionsService) -> None:
    logger.info("Received command subscriptions")

    trains = await subscriptions_service.get_subscribed_trains(message.chat.id)
    await send_trains(message, subscriptions_service, trains)
