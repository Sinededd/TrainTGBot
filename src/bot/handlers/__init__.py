from aiogram import Router

from bot.handlers import echo, start, auth

handlers_router = Router()
handlers_router.include_routers(
    # echo.router
    start.router,
    auth.router
)
