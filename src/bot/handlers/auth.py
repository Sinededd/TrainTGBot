import asyncio
import logging
import re

from aiogram import Bot
from aiogram import html, F
from typing import Dict, Any, Generator, List

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from bot.states.auth_states import AccountData, STATES_PERSONAL_LIST, StateUI
from bot.utils.sender import send_state_ui
from models.user import User
from services.user_service import UserService
from utils.crypto import encrypt_text

router = Router()


# Cancelling and go back flows
@router.message(Command("cancel"))
@router.message(F.text.casefold() == "отменить")
async def cancel_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    logging.debug(f"current_state: {current_state}")
    if current_state is None:
        return

    await try_mask_confirmation_message(state, bot, message.chat.id)

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.delete()
    await message.answer(
        "Галя отмена.",
        reply_markup=ReplyKeyboardRemove(),
    )


def get_previous_state(current_state: str) -> tuple[Any, Any, Any]:
    current_state_index = next(
        (i for i, obj in enumerate(STATES_PERSONAL_LIST) if obj.state_name == current_state),
        None,
    )
    previous_state_index = current_state_index - 1
    if previous_state_index < 0:
        return None, None, None
    return (
        STATES_PERSONAL_LIST[previous_state_index].state_name,
        STATES_PERSONAL_LIST[previous_state_index].state_question,
        STATES_PERSONAL_LIST[previous_state_index].keyboard_buttons,
    )


@router.message(Command("go back"))
@router.message(F.text.casefold() == "назад")
async def go_back_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("У вас нет активного процесса заполнения.")
        return

    await try_mask_confirmation_message(state, bot, message.chat.id)

    logging.info("Going back from %r", current_state)
    (
        previous_state,
        state_message,
        keyboard_buttons
    ) = get_previous_state(current_state)
    await message.delete()
    if previous_state is None:
        await message.answer(
            "Вы и так на первом шаге.",
        )
    else:
        await state.set_state(previous_state)
        await message.answer(
            state_message,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=keyboard_buttons,
                resize_keyboard=True,
            ),
        )


def get_buttons_for_states_excluding_confirm() -> List[Any]:
    return [
        state.state_corresponding_button
        for state in STATES_PERSONAL_LIST
        if state.state_name != AccountData.confirm and state.state_name is not None
    ]

def generate_confirmation_text(data: Dict[str, Any], mask: bool = False) -> str:
    """Generates a confirmation text based on the provided data. If mask=True, it hides the password and passport number."""
    passport = str(data.get('passport_number', ''))
    password = str(data.get('password', ''))

    if mask:
        passport = re.sub(r'\S', '*', passport) if passport else ''
        password = '*' * len(password) if password else ''

    return (
        f"{html.bold('Пожалуйста, проверьте ваши данные:')}\n\n"
        f"ФИО: {html.quote(str(data.get('surname', '')))} {html.quote(str(data.get('name', '')))} {html.quote(str(data.get('patronymic', '')))}\n"
        f"Номер паспорта: {html.quote(passport)}\n"
        f"Логин: {html.quote(str(data.get('login', '')))}\n"
        f"Пароль: {html.quote(password)}\n"
    )

async def try_mask_confirmation_message(state: FSMContext, bot: Bot, chat_id: int):
    """Safe hiding message if it hasn't been hidden yet."""
    data = await state.get_data()
    msg_id = data.get('confirmation_message_id')
    is_masked = data.get('is_masked', False)

    if msg_id and not is_masked:
        new_text = generate_confirmation_text(data, mask=True)
        try:
            await bot.edit_message_text(
                chat_id=chat_id,
                message_id=msg_id,
                text=new_text,
                parse_mode=ParseMode.HTML
            )
        except TelegramBadRequest as e:
            if "message is not modified" not in str(e).lower():
                logging.warning(f"Не удалось отредактировать сообщение {msg_id}: {e}")
        finally:
            await state.update_data(is_masked=True)


@router.message(AccountData.confirm)
async def hide_confidential_data_confirmation_ui(message: Message, state: FSMContext, bot: Bot, user_service: UserService) -> None:
    logging.info("Processing confirmation UI hiding")

    await try_mask_confirmation_message(state, bot, message.chat.id)

    if message.text:
        text = message.text.casefold()
        if text == "отклонить":
            await process_dont_confirm(message, state)
            return
        elif text == "подтвердить":
            await process_confirm(message, state, user_service)
            return

    await message.delete()


# disapprove handler
async def process_dont_confirm(message: Message, state: FSMContext) -> None:
    await state.set_state(AccountData.confirm_reject)
    keyboard_buttons = get_buttons_for_states_excluding_confirm()
    await message.delete()
    await message.answer(
        "Что заполнено неверно?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=button)
                    for button in keyboard_buttons[:(len(keyboard_buttons) + 1)//2]
                ],
                [
                    KeyboardButton(text=button)
                    for button in keyboard_buttons[(len(keyboard_buttons) + 1) // 2:]
                ],
                [
                    KeyboardButton(text="Отменить"),
                ],
            ],
            resize_keyboard=True,
        ),
    )

async def process_confirm(message: Message, state: FSMContext, user_service: UserService) -> None:
    await message.delete()

    data = await state.get_data()
    user = User(
        id=message.chat.id,
        surname=str(data.get('surname')),
        name=str(data.get('name')),
        patronymic=str(data.get('patronymic')),
        passport_number=encrypt_text(str(data.get('passport_number'))),
        login=str(data.get('login')),
        password=encrypt_text(str(data.get('password')))
    )

    await state.clear()

    if await user_service.register_user(user):
        await message.answer("Регистрация прошла успешно!", reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer("Данный пользователь уже зарегистрирован.", reply_markup=ReplyKeyboardRemove())


async def confirmation_ui(message: Message, state: FSMContext, hide_previous_message: bool = False):
    """Send ui for confirmation form"""
    if hide_previous_message:
        await message.delete()
        await message.answer(text="Данные скрыты")

    await state.set_state(AccountData.confirm)
    data = await state.get_data()

    # Генерируем открытый текст
    text = generate_confirmation_text(data, mask=False)

    sent_msg = await message.answer(
        text,
        parse_mode=ParseMode.HTML
    )

    await message.answer(
        text="Пожалуйста, подтвердите или отклоните данные.",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Подтвердить"), KeyboardButton(text="Отклонить")],
                [KeyboardButton(text="Назад")],
                [KeyboardButton(text="Отменить")],
            ],
            resize_keyboard=True,
        ),
    )

    await state.update_data(
        confirmation_message_id=sent_msg.message_id,
        is_masked=False
    )


@router.message(AccountData.confirm_reject, F.text.casefold() != "отменить")
async def process_reject(message: Message, state: FSMContext) -> None:
    required_state_index = next(
        (
            i
            for i, obj in enumerate(STATES_PERSONAL_LIST)
            if obj.state_corresponding_button == message.text
        ),
        None,
    )
    await message.delete()
    if required_state_index is None:
        await message.answer(
            "Я вас не понял. Пожалуйста повторите выбор."
        )
    else:
        required_state = STATES_PERSONAL_LIST[required_state_index]
        await state.update_data(reject=True)
        await state.set_state(required_state.state_name)
        await message.answer(
            required_state.state_question,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=required_state.keyboard_buttons,
                resize_keyboard=True,
            ),
        )


# Handlers for each state

@router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    if (await state.get_data()).get("reject", False):
        await confirmation_ui(message, state)
    else:
        await state.set_state(AccountData.surname)
        await send_state_ui(message, AccountData.surname)


@router.message(AccountData.surname)
async def process_surname(message: Message, state: FSMContext) -> None:
    await state.update_data(surname=message.text)
    if (await state.get_data()).get("reject", False):
        await confirmation_ui(message, state)
    else:
        await state.set_state(AccountData.name)
        await send_state_ui(message, AccountData.name)


@router.message(AccountData.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    if (await state.get_data()).get("reject", False):
        await confirmation_ui(message, state)
    else:
        await state.set_state(AccountData.patronymic)
        await send_state_ui(message, AccountData.patronymic)


@router.message(AccountData.patronymic)
async def process_patronymic(message: Message, state: FSMContext) -> None:
    await state.update_data(patronymic=message.text)
    if (await state.get_data()).get("reject", False):
        await confirmation_ui(message, state)
    else:
        await state.set_state(AccountData.passport_number)
        await send_state_ui(message, AccountData.passport_number)


@router.message(AccountData.passport_number)
async def process_passport_number(message: Message, state: FSMContext) -> None:
    await state.update_data(passport_number=message.text)
    if (await state.get_data()).get("reject", False):
        await confirmation_ui(message, state, True)
    else:
        await state.set_state(AccountData.login)
        await send_state_ui(message, AccountData.login, True)


@router.message(AccountData.login)
async def process_login(message: Message, state: FSMContext) -> None:
    await state.update_data(login=message.text)
    if (await state.get_data()).get("reject", False):
        await confirmation_ui(message, state)
    else:
        await state.set_state(AccountData.password)
        await send_state_ui(message, AccountData.password)


@router.message(AccountData.password)
async def process_password(message: Message, state: FSMContext) -> None:
    await state.update_data(password=message.text)
    await confirmation_ui(message, state, True)
