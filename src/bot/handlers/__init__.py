from aiogram import Router

from bot.handlers import echo

handlers_router = Router()
handlers_router.include_routers(
    echo.router
)
