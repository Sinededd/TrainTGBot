import asyncio
import json
import logging
from datetime import date

from dotenv import load_dotenv
from playwright.async_api import async_playwright, Playwright

from bot.bot import start_bot
from db.sqlite_user_repository import SQLiteUserRepository
from services import seats_extractor
from services.parser import Parser
from repository.pickle_train_repository import PickleTrainRepository
from services.user_service import UserService


async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=False, slow_mo=100)
    context = await browser.new_context()

    pickle_tr_repo = PickleTrainRepository("trains.pkl")
    parser = Parser(context, pickle_tr_repo)
    await parser.login()

    # ---------------------
    # trains = await parser.get_trains("Минск", "Лунинец", date(2026, 7, 25))
    # for train in trains:
    #     pickle_tr_repo.save(train)
    #     print(train)
    #     print(train.id)
    #     print(train.tariffs)
    #     print("-----------------------")
    train_id = "1_859Б_1784977080_1784989140"

    train_data = await parser.get_train_data(train_id)
    seats = seats_extractor.extract_seats(train_data)
    seat = seats.get_first(lambda x: not x.hasTable and x.price < 30)
    print(json.dumps(seat, indent=2, ensure_ascii=False, default=str))

    if seat:
        await parser.choose_train(train_id)
        await parser.choose_seat(seat)
        await parser.place_an_order("Гришко", "Денис", "Михайлович", "AB1111111")

    # ---------------------

    await context.close()
    await browser.close()


async def main():
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)

    # Configure db
    user_repo = SQLiteUserRepository(db_path="database.db")
    await user_repo.init_db()
    user_service = UserService(user_repo=user_repo)

    #Start bot
    await start_bot(user_service=user_service)

    # async with async_playwright() as playwright:
    #     await run(playwright)


if __name__ == '__main__':
    asyncio.run(main())