from models.train import Train
from repository.subscriptions_repository import SubscriptionsRepository
from services.train_service import TrainService


class SubscriptionsService:
    def __init__(self, subscriptions_repo: SubscriptionsRepository, train_service: TrainService):
        self.subscriptions_repo = subscriptions_repo
        self.train_service = train_service

    async def subscribe(self, user_id: int, train_id: str) -> None:
        await self.subscriptions_repo.add(user_id, train_id)

    async def unsubscribe(self, user_id: int, train_id: str) -> None:
        await self.subscriptions_repo.remove(user_id, train_id)

    async def check_subscription(self, user_id: int, train_id: str) -> bool:
        return await self.subscriptions_repo.check(user_id, train_id)

    async def get_subscribed_trains(self, user_id: int) -> list[Train]:
        train_ids = await self.subscriptions_repo.get_all_by_user_id(user_id)
        trains : list[Train] = []
        for train_id in train_ids:
            train = await self.train_service.search_train(train_id)
            if train:
                trains.append(train)
        return trains