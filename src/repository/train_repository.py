from abc import ABC, abstractmethod

from dto.train_entity import TrainEntity
from src.models.train import Train


class TrainRepository(ABC):
    """Interface for train repository"""

    @abstractmethod
    async def add(self, train: Train) -> None:
        """Add train to database or ignore if already exists"""
        pass

    @abstractmethod
    async def get_by_id(self, train_id: str) -> TrainEntity | None:
        """Get train by id"""
        pass

    @abstractmethod
    async def delete_expired(self) -> int:
        """Delete all expired trains and return number of deleted trains"""
        pass
