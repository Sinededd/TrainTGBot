from aiogram.fsm.state import StatesGroup, State


class SearchParams(StatesGroup):
    from_station = State()
    to_station = State()
    date = State()