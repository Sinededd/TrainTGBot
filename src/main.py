import asyncio
from datetime import date

from playwright.async_api import async_playwright, Playwright, BrowserContext

from parser import Parser


async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=False, slow_mo=100)
    context = await browser.new_context()

    parser = Parser(context)
    await parser.login()
    # ---------------------
    print(await parser.get_trains("Минск", "Лунинец", date(2026, 7, 24)))
    # ---------------------

    await context.close()
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == '__main__':
    asyncio.run(main())