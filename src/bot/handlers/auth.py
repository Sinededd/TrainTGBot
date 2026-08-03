import logging

from aiogram import html, F
from typing import Dict, Any, Generator, List

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from bot.states.auth_states import PersonalData, STATES_LIST, StateUI
from bot.utils.sender import send_state_ui

router = Router()


# Cancelling and go back flows
@router.message(Command("cancel"))
@router.message(F.text.casefold() == "отменить")
async def cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Allow user to cancel any action
    """
    current_state = await state.get_state()
    logging.debug(f"current_state: {current_state}")
    if current_state is None:
        return

    logging.info("Cancelling state %r", current_state)
    await state.clear()
    await message.answer(
        "Галя отмена.",
        reply_markup=ReplyKeyboardRemove(),
    )


def get_previous_state(current_state: str) -> tuple[Any, Any, Any]:
    current_state_index = next(
        (i for i, obj in enumerate(STATES_LIST) if obj.state_name == current_state),
        None,
    )
    previous_state_index = current_state_index - 1
    if previous_state_index < 0:
        return None, None, None
    return (
        STATES_LIST[previous_state_index].state_name,
        STATES_LIST[previous_state_index].state_question,
        STATES_LIST[previous_state_index].keyboard_buttons,
    )


@router.message(Command("go back"))
@router.message(F.text.casefold() == "назад")
async def go_back_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("У вас нет активного процесса заполнения.")
        return
    logging.info("Going back from %r", current_state)
    (
        previous_state,
        state_message,
        keyboard_buttons
    ) = get_previous_state(current_state)
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
        for state in STATES_LIST
        if state.state_name != PersonalData.confirm and state.state_name is not None
    ]


# disapprove handler
@router.message(PersonalData.confirm, F.text.casefold() == "отклонить")
async def process_dont_confirm(message: Message, state: FSMContext) -> None:
    await state.set_state(PersonalData.confirm_reject)
    await message.answer(
        "Что заполнено неверно?",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=button)
                    for button in get_buttons_for_states_excluding_confirm()
                ],
                [
                    KeyboardButton(text="Отменить"),
                ],
            ],
            resize_keyboard=True,
        ),
    )

@router.message(PersonalData.confirm_reject, F.text.casefold() != "отменить")
async def process_reject(message: Message, state: FSMContext) -> None:
    required_state_index = next(
        (
            i
            for i, obj in enumerate(STATES_LIST)
            if obj.state_corresponding_button == message.text
        ),
        None,
    )
    if required_state_index is None:
        await message.answer(
            "Я вас не понял. Пожалуйста повторите выбор."
        )
    else:
        required_state = STATES_LIST[required_state_index]
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
        await state.set_state(PersonalData.surname)
        await send_state_ui(message, PersonalData.surname)

@router.message(PersonalData.surname)
async def process_surname(message: Message, state: FSMContext) -> None:
    await state.update_data(surname=message.text)
    if (await state.get_data()).get("reject", False):
        await confirmation_ui(message, state)
    else:
        await state.set_state(PersonalData.name)
        await send_state_ui(message, PersonalData.name)


@router.message(PersonalData.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    if (await state.get_data()).get("reject", False):
        await confirmation_ui(message, state)
    else:
        await state.set_state(PersonalData.patronymic)
        await send_state_ui(message, PersonalData.patronymic)


@router.message(PersonalData.patronymic)
async def process_patronymic(message: Message, state: FSMContext) -> None:
    await state.update_data(patronymic=message.text)
    if (await state.get_data()).get("reject", False):
        await confirmation_ui(message, state)
    else:
        await state.set_state(PersonalData.passport_number)
        await send_state_ui(message, PersonalData.passport_number)


async def confirmation_ui(message: Message, state: FSMContext):
    await state.set_state(PersonalData.confirm)
    data: Dict[str, Any] = await state.get_data()
    await message.answer(
        f"{html.bold('Пожалуйста, проверьте ваши данные:')}\n\n"
        f"ФИО: {html.quote(data['surname'])} {html.quote(data['name'])} {html.quote(data['patronymic'])}\n"
        f"Номер паспорта: {html.quote(data['passport_number'])}\n",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Подтвердить"), KeyboardButton(text="Отклонить")],
                [KeyboardButton(text="Назад")],
                [KeyboardButton(text="Отменить")],
            ],
            resize_keyboard=True,
        ),
        parse_mode=ParseMode.HTML
    )


@router.message(PersonalData.passport_number)
async def process_passport_number(message: Message, state: FSMContext) -> None:
    await state.update_data(passport_number=message.text)
    await confirmation_ui(message, state)


@router.message(PersonalData.confirm, F.text.casefold() == "подтвердить")
async def process_confirm(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        "Спасибо за заполнение формы!",
        reply_markup=ReplyKeyboardRemove(),
    )
