from abc import abstractmethod, ABC
from typing import List


class SubscriptionsRepository(ABC):

    @abstractmethod
    async def add(self, user_id: int, train_id: str) -> None:
        pass

    @abstractmethod
    async def remove(self, user_id: int, train_id: str) -> None:
        pass

    @abstractmethod
    async def check(self, user_id: int, train_id: str) -> bool:
        pass

    @abstractmethod
    async def get_all_by_user_id(self, user_id: int) -> List[str]:
        """Return all train ids belonging to the given user_id"""
        pass

    @abstractmethod
    async def get_all_by_train_id(self, train_id: str) -> List[int]:
        """Return all user ids belonging to the given train_id"""
        pass
