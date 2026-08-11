from domain.models.subscription import Subscription
from domain.models.train import Train
from repository.subscriptions_repository import SubscriptionsRepository
from services.train_service import TrainService


class SubscriptionsService:
    def __init__(self, subscriptions_repo: SubscriptionsRepository, train_service: TrainService):
        self.subscriptions_repo = subscriptions_repo
        self.train_service = train_service

    async def subscribe(self, subscription: Subscription) -> None:
        await self.subscriptions_repo.add(subscription)

    async def unsubscribe(self, subscription: Subscription) -> None:
        await self.subscriptions_repo.remove(subscription)

    async def check_subscription(self, subscription: Subscription) -> bool:
        return await self.subscriptions_repo.check(subscription)

    async def get_subscribed_trains(self, user_id: int) -> list[Train]:
        train_ids = await self.subscriptions_repo.get_all_by_user_id(user_id)
        trains : list[Train] = []
        for train_id in train_ids:
            train = await self.train_service.search_train(train_id)
            if train:
                trains.append(train)
        return trains