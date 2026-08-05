import logging

from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from bot.states.search_train_state import SearchParams
from services.parser import get_trains
from utils.convert_data import convert_to_iso

router = Router()


@router.message(Command("schedule"))
async def command_schedule(message: Message, state: FSMContext) -> None:
    await state.set_state(SearchParams.from_station)
    await message.answer(text="Введите станцию отправления:")


@router.message(SearchParams.from_station)
async def process_from_station(message: Message, state: FSMContext) -> None:
    await state.update_data(from_station=message.text)
    await state.set_state(SearchParams.to_station)
    await message.answer(text="Введите станцию прибытия:")

@router.message(SearchParams.to_station)
async def process_to_station(message: Message, state: FSMContext) -> None:
    await state.update_data(to_station=message.text)
    await state.set_state(SearchParams.date)
    await message.answer(text="Введите дату отправления:")

@router.message(SearchParams.date)
async def process_date(message: Message, state: FSMContext) -> None:
    date = convert_to_iso(message.text)
    if date is None:
        await message.answer(text="Неверный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ:")
        return

    data = await state.get_data()
    from_station = str(data.get('from_station'))
    to_station = str(data.get('to_station'))
    trains = await get_trains(from_station, to_station, date)
    logging.debug("Trains: %s", trains)
    for train in trains:
        await message.answer(
            train.to_html(),
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="Подписаться",
                            callback_data=f"subscribe:{train.id}"
                        )
                    ]
                ]
            )
        )

    await state.clear()

