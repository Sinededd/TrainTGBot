import asyncio
from playwright.async_api import async_playwright, Playwright, BrowserContext

from parser import Parser


async def run(playwright: Playwright) -> None:
    browser = await playwright.chromium.launch(headless=False, slow_mo=100)
    context = await browser.new_context()

    parser = Parser(context)
    await parser.login()
    # ---------------------

    await context.close()
    await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == '__main__':
    asyncio.run(main())