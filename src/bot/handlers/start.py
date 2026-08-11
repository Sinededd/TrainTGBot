from aiogram import Router, html
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.enums import ParseMode

from bot.states.auth_states import AccountData
from bot.handlers.auth_views import send_state_ui
from services.user_service import UserService

router = Router()


@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext, user_service: UserService) -> None:
    user_id = message.chat.id
    user = await user_service.get_user(user_id)

    await state.clear()

    if user:
        greeting_text = (
            f"👋 {html.bold('Добро пожаловать')} {html.code(user.name)}!\n\n"
            f"🚆 {html.italic('Бот для поиска и бронирования поездов')}\n\n"
            f"{html.bold('Доступные команды:')}\n"
            f"/schedule - 🔍 Поиск поездов\n"
            f"/subscriptions - ⭐ Мои подписки\n"
            f"/account - 👤 Изменение персональных данных"
        )

        await message.answer(
            greeting_text,
            parse_mode=ParseMode.HTML
        )
    else:
        greeting_text = (
            f"👋 {html.bold('Привет!')}\n\n"
            f"Я помогу вам найти и забронировать поезд. "
            f"Давайте начнём с регистрации! /account"
        )

        await message.answer(
            greeting_text,
            parse_mode=ParseMode.HTML
        )