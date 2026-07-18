from abc import ABC, abstractmethod

from src.models.train import Train


class TrainRepository(ABC):
    """Интерфейс для доступа к хранилищу поездов"""

    @abstractmethod
    def get_by_id(self, train_id: str) -> Train:
        """Получить поезд по ID"""
        pass

    @abstractmethod
    def save(self, train: Train) -> None:
        """Сохранить поезд"""
        pass