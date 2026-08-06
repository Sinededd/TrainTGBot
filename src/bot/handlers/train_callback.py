from venv import logger

from aiogram import Router
from aiogram.filters.callback_data import CallbackData
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message
from aiogram.utils.keyboard import InlineKeyboardBuilder


router = Router()


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


@router.callback_query(TrainSubscribeCallback.filter())
async def toggle_subscription(callback: CallbackQuery, callback_data: TrainSubscribeCallback):
    new_status = not callback_data.is_subscribed

    #  Logic of saving in db:
    # await db.set_user_subscription(user_id=callback.from_user.id, train_id=callback_data.train_id, status=new_status)

    new_keyboard = get_train_keyboard(
        train_id=callback_data.train_id,
        is_subscribed=new_status
    )

    if not isinstance(callback.message, Message):
        await callback.answer("Сообщение больше недоступно", show_alert=True)
        return


    await callback.message.edit_reply_markup(reply_markup=new_keyboard)
    logger.info(f"Callback: User {callback.message.chat.id} subscribed to train {callback_data.train_id}")