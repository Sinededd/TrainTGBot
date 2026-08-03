from dataclasses import dataclass

from aiogram.fsm.state import StatesGroup, State
from aiogram.types import KeyboardButton


class AccountData(StatesGroup):
    name = State()
    surname = State()
    patronymic = State()
    passport_number = State()
    login = State()
    password = State()
    confirm = State()
    confirm_reject = State()


@dataclass
class StateUI:
    state_name: State
    state_question: str
    state_in_memory_name: str
    state_corresponding_button: str
    keyboard_buttons: list[list[KeyboardButton]]


STATES_PERSONAL_LIST = [
    StateUI(
        state_name=AccountData.surname,
        state_question="Введите свою фамилию:",
        state_in_memory_name="surname",
        state_corresponding_button="Фамилия",
        keyboard_buttons=[
            [KeyboardButton(text="Отменить")]
        ]
    ),
    StateUI(
        state_name=AccountData.name,
        state_question="Введите свое имя:",
        state_in_memory_name="name",
        state_corresponding_button="Имя",
        keyboard_buttons=[
            [KeyboardButton(text="Назад")],
            [KeyboardButton(text="Отменить")]
        ]
    ),
    StateUI(
        state_name=AccountData.patronymic,
        state_question="Введите свое отчество:",
        state_in_memory_name="patronymic",
        state_corresponding_button="Отчество",
        keyboard_buttons=[
            [KeyboardButton(text="Назад")],
            [KeyboardButton(text="Отменить")]
        ]
    ),
    StateUI(
        state_name=AccountData.passport_number,
        state_question="Введите свой номер паспорта:",
        state_in_memory_name="passport_number",
        state_corresponding_button="Номер паспорта",
        keyboard_buttons=[
            [KeyboardButton(text="Назад")],
            [KeyboardButton(text="Отменить")]
        ]
    ),
    StateUI(
        state_name=AccountData.login,
        state_question="Введите логин:",
        state_in_memory_name="login",
        state_corresponding_button="Логин",
        keyboard_buttons=[
            [KeyboardButton(text="Назад")],
            [KeyboardButton(text="Отменить")]
        ]
    ),
    StateUI(
        state_name=AccountData.password,
        state_question="Введите пароль:",
        state_in_memory_name="password",
        state_corresponding_button="Пароль",
        keyboard_buttons=[
            [KeyboardButton(text="Назад")],
            [KeyboardButton(text="Отменить")]
        ]
    ),
    StateUI(
        state_name=AccountData.confirm,
        state_question="",
        state_in_memory_name="",
        state_corresponding_button="",
        keyboard_buttons=[
            [KeyboardButton(text="Подтвердить"),
             KeyboardButton(text="Отклонить")],
            [KeyboardButton(text="Назад")],
            [KeyboardButton(text="Отменить")],
        ]
    )
]
