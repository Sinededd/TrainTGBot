from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.handlers.train_views import send_trains
from bot.states.search_train_state import SearchParams
from domain.exceptions import NoTrainsFoundException
from services.subscriptions_service import SubscriptionsService
from services.train_service import TrainService
from utils.convert_date_time import convert_to_iso

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
async def process_date(message: Message, state: FSMContext, train_service: TrainService, subscriptions_service: SubscriptionsService) -> None:
    date = convert_to_iso(message.text)
    if date is None:
        await message.answer(text="Неверный формат даты. Пожалуйста, введите дату в формате ДД.ММ.ГГГГ:")
        return

    data = await state.get_data()
    await state.clear()
    from_station = str(data.get('from_station'))
    to_station = str(data.get('to_station'))

    try:
        trains = await train_service.search_trains(from_station, to_station, date)
        await send_trains(message, subscriptions_service, trains)

    except NoTrainsFoundException as e:
        await message.answer(str(e))