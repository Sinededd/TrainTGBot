import asyncio
import logging

from playwright.async_api import async_playwright

from bot.bot import start_bot
from infrastructure.db.connection import init_db
from infrastructure.db.repositories.sqlite_subscriptions_repository import SQLiteSubscriptionsRepository
from infrastructure.db.repositories.sqlite_train_repository import SQLiteTrainRepository
from infrastructure.db.repositories.sqlite_user_repository import SQLiteUserRepository
from services.subscriptions_service import SubscriptionsService
from services.train_service import TrainService
from services.user_service import UserService


async def main():
    # Configure logging
    logging.basicConfig(level=logging.DEBUG)

    # Configure playwright

    # Configure db
    await init_db()
    user_repo = SQLiteUserRepository()
    user_service = UserService(user_repo=user_repo)
    train_repo = SQLiteTrainRepository()
    train_service = TrainService(train_repo=train_repo)
    subscriptions_repo = SQLiteSubscriptionsRepository()
    subscriptions_service = SubscriptionsService(subscriptions_repo=subscriptions_repo, train_service=train_service)

    # Start bot
    async with async_playwright() as playwright:
        await start_bot(
            playwright=playwright,
            user_service=user_service,
            train_service=train_service,
            subscriptions_service=subscriptions_service,
            train_repository=train_repo,
        )


if __name__ == '__main__':
    asyncio.run(main())
