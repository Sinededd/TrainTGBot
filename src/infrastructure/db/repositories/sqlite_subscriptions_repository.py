from typing import List

from infrastructure.db.connection import DEFAULT_DB_PATH, get_db
from domain.models.subscription import Subscription
from repository.subscriptions_repository import SubscriptionsRepository


class SQLiteSubscriptionsRepository(SubscriptionsRepository):

    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path

    async def add(self, subscription: Subscription):
        async with get_db(self.db_path) as db:
            await db.execute(
                """
                INSERT OR IGNORE INTO subscriptions (user_id, train_id)
                VALUES (?, ?)
                """,
                (subscription.user_id, subscription.train_id)
            )
            await db.commit()

    async def remove(self, subscription: Subscription):
        async with get_db(self.db_path) as db:
            await db.execute(
                "DELETE FROM subscriptions WHERE user_id=? AND train_id=?",
                (subscription.user_id, subscription.train_id)
            )
            await db.commit()

    async def check(self, subscription: Subscription) -> bool:
        async with get_db(self.db_path) as db:
            cursor = await db.execute(
                "SELECT * FROM subscriptions WHERE user_id=? AND train_id=?",
                (subscription.user_id, subscription.train_id)
            )
            return await cursor.fetchone() is not None

    async def get_all_by_user_id(self, user_id: int) -> List[str]:
        async with get_db(self.db_path) as db:
            cursor = await db.execute(
                "SELECT train_id FROM subscriptions WHERE user_id=?",
                (user_id,)
            )
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

    async def get_all_by_train_id(self, train_id: str) -> List[int]:
        async with get_db(self.db_path) as db:
            cursor = await db.execute(
                "SELECT user_id FROM subscriptions WHERE train_id=?",
                (train_id,)
            )
            rows = await cursor.fetchall()
            return [row[0] for row in rows]

    async def get_all(self) -> list[Subscription]:
        async with get_db(self.db_path) as db:
            cursor = await db.execute(
                "SELECT user_id, train_id FROM subscriptions",
            )
            rows = await cursor.fetchall()
            return [Subscription(row[0], row[1]) for row in rows]
