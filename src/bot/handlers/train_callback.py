from venv import logger

from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, Message

from bot.handlers.train_views import get_train_keyboard, TrainSubscribeCallback
from models.subscription import Subscription
from services.subscriptions_service import SubscriptionsService

router = Router()


@router.callback_query(TrainSubscribeCallback.filter())
async def toggle_subscription(callback: CallbackQuery, callback_data: TrainSubscribeCallback,
                              subscriptions_service: SubscriptionsService):
    new_status = not callback_data.is_subscribed

    new_keyboard = get_train_keyboard(
        train_id=callback_data.train_id,
        is_subscribed=new_status
    )

    if not isinstance(callback.message, Message):
        await callback.answer("Сообщение больше недоступно", show_alert=True)
        return

    if new_status:
        await subscriptions_service.subscribe(Subscription(callback.from_user.id, callback_data.train_id))
    else:
        await subscriptions_service.unsubscribe(Subscription(callback.from_user.id, callback_data.train_id))

    await callback.message.edit_reply_markup(reply_markup=new_keyboard)
    logger.info(f"Callback: User {callback.message.chat.id} subscribed to train {callback_data.train_id}")
