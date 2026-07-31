from aiogram.fsm.state import StatesGroup, State


class PersonalData(StatesGroup):
    name = State()
    surname = State()
    patronymic = State()
    passportNumber = State()

class AccountData(StatesGroup):
    login = State()
    password = State()

class Form(StatesGroup):
    personal_data = PersonalData
    confirm_personal_data = State()
    account_data = AccountData
    confirm_account_data = State()