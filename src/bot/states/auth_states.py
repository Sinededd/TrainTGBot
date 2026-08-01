from dataclasses import dataclass

from aiogram.fsm.state import StatesGroup, State
from aiogram.types import KeyboardButton


class PersonalData(StatesGroup):
    name = State()
    surname = State()
    patronymic = State()
    passport_number = State()
    confirm = State()


class AccountData(StatesGroup):
    login = State()
    password = State()


@dataclass
class StateUI:
    state_name: State
    state_question: str
    state_in_memory_name: str
    state_corresponding_button: str
    keyboard_buttons: list[list[KeyboardButton]]


STATES_LIST = [
    StateUI(
        state_name=PersonalData.surname,
        state_question="Введите свою фамилию:",
        state_in_memory_name="surname",
        state_corresponding_button="Фамилия",
        keyboard_buttons=[
            [KeyboardButton(text="Отменить")]
        ]
    ),
    StateUI(
        state_name=PersonalData.name,
        state_question="Введите свое имя:",
        state_in_memory_name="name",
        state_corresponding_button="Имя",
        keyboard_buttons=[
            [KeyboardButton(text="Назад")],
            [KeyboardButton(text="Отменить")]
        ]
    ),
    StateUI(
        state_name=PersonalData.patronymic,
        state_question="Введите свое отчество:",
        state_in_memory_name="patronymic",
        state_corresponding_button="Отчество",
        keyboard_buttons=[
            [KeyboardButton(text="Назад")],
            [KeyboardButton(text="Отменить")]
        ]
    ),
    StateUI(
        state_name=PersonalData.passport_number,
        state_question="Введите свой номер паспорта:",
        state_in_memory_name="passport_number",
        state_corresponding_button="Номер паспорта",
        keyboard_buttons=[
            [KeyboardButton(text="Назад")],
            [KeyboardButton(text="Отменить")]
        ]
    ),
    StateUI(
        state_name=PersonalData.confirm,
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
