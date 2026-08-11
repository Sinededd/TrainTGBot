from abc import abstractmethod, ABC

from domain.models.subscription import Subscription


class SubscriptionsRepository(ABC):

    @abstractmethod
    async def add(self, subscription: Subscription) -> None:
        pass

    @abstractmethod
    async def remove(self, subscription: Subscription) -> None:
        pass

    @abstractmethod
    async def check(self, subscription: Subscription) -> bool:
        pass

    @abstractmethod
    async def get_all_by_user_id(self, user_id: int) -> list[str]:
        """Return all train ids belonging to the given user_id"""
        pass

    @abstractmethod
    async def get_all_by_train_id(self, train_id: str) -> list[int]:
        """Return all user ids belonging to the given train_id"""
        pass

    @abstractmethod
    async def get_all(self) -> list[Subscription]:
        """Return all subscriptions as a list of tuples (user_id, train_id)"""
