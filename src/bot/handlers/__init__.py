from aiogram import Router

from bot.handlers import echo, start, auth, search_train

handlers_router = Router()
handlers_router.include_routers(
    # echo.router
    start.router,
    auth.router,
    search_train.router
)
