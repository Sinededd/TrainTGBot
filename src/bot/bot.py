import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
load_dotenv()
api_token = os.getenv("API_TOKEN")
if api_token is None:
    raise ValueError("API_TOKEN not found in .env file")
bot = Bot(token=api_token)
dp = Dispatcher()


# Request to get trains machine
# get_trains_state =

@dp.message()
async def echo(message):

    await message.answer(message.text)