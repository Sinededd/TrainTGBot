from aiogram.enums import ParseMode
from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

from models.subscription import Subscription
from models.train import Train
from services.subscriptions_service import SubscriptionsService


class TrainSubscribeCallback(CallbackData, prefix="sub_train"):
    train_id: str
    is_subscribed: bool


def get_train_keyboard(train_id: str, is_subscribed: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if is_subscribed:
        builder.button(
            text="🔕 Отписаться",
            callback_data=TrainSubscribeCallback(train_id=train_id, is_subscribed=True).pack()
        )
    else:
        builder.button(
            text="🔔 Подписаться",
            callback_data=TrainSubscribeCallback(train_id=train_id, is_subscribed=False).pack()
        )

    return builder.as_markup()


async def send_trains(message: Message, subscriptions_service: SubscriptionsService, trains: list[Train]) -> None:
    if not trains:
        await message.answer("Поездов не найдено")
        return

    for train in trains:
        await message.answer(
            train.to_html(),
            parse_mode=ParseMode.HTML,
            reply_markup=get_train_keyboard(train.id,
                                            await subscriptions_service.check_subscription(Subscription(message.chat.id, train.id))),
        )
