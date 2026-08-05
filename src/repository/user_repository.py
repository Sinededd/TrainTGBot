from abc import ABC, abstractmethod
from typing import Sequence

from models.user import User


class UserRepository(ABC):

    @abstractmethod
    async def add(self, user: User) -> None:
        """Create and save a new user"""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: int) -> User | None:
        """Return user by id"""
        pass

    async def list_all(self) -> Sequence[User]:
        """Return all users"""
        pass

