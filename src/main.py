import asyncio
from datetime import date

from playwright.async_api import async_playwright, Playwright

import seats_extractor
from models import tariffs, available_seats
from src.parser import Parser
from repository.pickle_train_repository import PickleTrainRepository


async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=False, slow_mo=100)
    context = await browser.new_context()

    pickle_tr_repo = PickleTrainRepository("trains.pkl")
    parser = Parser(context, pickle_tr_repo)
    await parser.login()

    # ---------------------
    trains = await parser.get_trains("Минск", "Лунинец", date(2026, 7, 25))

    for train in trains:
        pickle_tr_repo.save(train)
        print(train)
        print(train.tariffs)
        print("-----------------------")

    train_data = await parser.get_train_data(train_id=trains[1].id)
    print(seats_extractor.extract_seats(train_data))
    # ---------------------

    await context.close()
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == '__main__':
    asyncio.run(main())