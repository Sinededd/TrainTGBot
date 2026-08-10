from aiogram import Router

from bot.handlers import echo, start, auth, search_train, train_callback, subscriptions

handlers_router = Router()
handlers_router.include_routers(
    # echo.router
    start.router,
    auth.router,
    search_train.router,
    train_callback.router,
    subscriptions.router,
)
