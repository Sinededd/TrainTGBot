import os

from playwright.async_api import BrowserContext
from dotenv import load_dotenv

load_dotenv()

class Parser:
    def __init__(self, context: BrowserContext):
        self.context = context

    async def login(self):
        page = await self.context.new_page()
        await page.goto("https://pass.rw.by/ru/")
        await page.get_by_role("button", name="Принять").click()
        await page.get_by_role("link", name="Личный кабинет").click()


        login_val = os.getenv("BY_LOGIN")
        password_val = os.getenv("BY_PASSWORD")
        if not login_val or not password_val:
            raise ValueError(
                "Error:  BY_LOGIN or BY_PASSWORD not found in dotenv! "
                "Check your dotenv file and try again."
            )

        await page.get_by_role("textbox", name="Логин/E-mail").fill(login_val)
        await page.get_by_role("textbox", name="Пароль").fill(password_val)
        await page.get_by_role("button", name="Войти").click()

        await page.pause()
