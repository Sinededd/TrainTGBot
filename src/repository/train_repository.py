from abc import ABC, abstractmethod

from src.models.train import Train


class TrainRepository(ABC):
    """Interface for train repository"""

    @abstractmethod
    def get_by_id(self, train_id: str) -> Train:
        pass

    @abstractmethod
    def add(self, train: Train) -> None:
        pass