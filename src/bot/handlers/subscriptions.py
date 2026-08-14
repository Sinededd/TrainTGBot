import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from bot.handlers.train_views import send_trains
from services.subscriptions_service import SubscriptionsService
from services.user_service import UserService

logger = logging.getLogger(__name__)
router = Router()


@router.message(Command("subscriptions"))
async def command_subscriptions(message: Message, subscriptions_service: SubscriptionsService,
                                user_service: UserService) -> None:
    logger.info("Received command subscriptions")
    user = await user_service.get_user(message.chat.id)
    if not user:
        await message.answer("Вы не зарегистрированы. Пожалуйста, используйте команду /account для регистрации.")
        return

    trains = await subscriptions_service.get_subscribed_trains(message.chat.id)
    await send_trains(message, subscriptions_service, trains)
