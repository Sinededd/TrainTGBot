from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

from bot.states.auth_states import AccountData
from bot.utils.sender import send_state_ui

router = Router()

# @router.message(CommandStart())
# async def command_start(message: Message, state: FSMContext) -> None:
#
