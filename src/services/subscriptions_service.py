from repository.subscriptions_repository import SubscriptionsRepository
from repository.user_repository import UserRepository


class SubscriptionsService:
    def __init__(self, subscriptions_repo: SubscriptionsRepository):
        self.subscriptions_repo = subscriptions_repo

    async def subscribe(self, user_id: int, train_id: str) -> None:
        await self.subscriptions_repo.add(user_id, train_id)

    async def unsubscribe(self, user_id: int, train_id: str) -> None:
        await self.subscriptions_repo.remove(user_id, train_id)

    async def check_subscription(self, user_id: int, train_id: str) -> bool:
        return await self.subscriptions_repo.check(user_id, train_id)