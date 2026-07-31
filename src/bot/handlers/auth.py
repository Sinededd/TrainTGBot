from aiogram import html
from typing import Dict, Any

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from bot.states.auth_states import Form

router = Router()

@router.message(Form.personal_data.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Form.personal_data.surname)
    await message.answer(
        "Введите свою фамилию",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Назад")],
                [KeyboardButton(text="Отменить")]
            ],
            resize_keyboard=True,
        ),
    )


@router.message(Form.personal_data.surname)
async def process_surname(message: Message, state: FSMContext) -> None:
    await state.update_data(surname=message.text)
    await state.set_state(Form.personal_data.patronymic)
    await message.answer(
        "Введите свое отчество",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Назад")],
                [KeyboardButton(text="Отменить")]
            ],
            resize_keyboard=True,
        ),
    )

@router.message(Form.personal_data.patronymic)
async def process_patronymic(message: Message, state: FSMContext) -> None:
    await state.update_data(patronymic=message.text)
    await state.set_state(Form.personal_data.passportNumber)
    await message.answer(
        "Введите свой номер паспорта",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Назад")],
                [KeyboardButton(text="Отменить")]
            ],
            resize_keyboard=True,
        ),
    )


@router.message(Form.personal_data.passportNumber)
async def process_passport_number(message: Message, state: FSMContext) -> None:
    await state.update_data(passport_number=message.text)
    await state.set_state(Form.confirm_personal_data)
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

# @router.message(Form.personal_data.passportNumber)
# async def process_passport_number(message: Message, state: FSMContext) -> None:
#     await state.update_data(passport_number=message.text)
#     await state.set_state(Form.account_data.login)
#     await message.answer(
#         "Чтобы бот мог автоматически бронировать билеты, введите логин и пароль от аккаунта БЖД\n\nВведите логин",
#         reply_markup=ReplyKeyboardMarkup(
#             keyboard=[
#                 [KeyboardButton(text="Назад")],
#                 [KeyboardButton(text="Отменить")]
#             ],
#             resize_keyboard=True,
#         ),
#     )