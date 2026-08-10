from gettext import find

from domain.models.train import Train
from repository.train_repository import TrainRepository
from infrastructure.parser.rw_parser import Parser


class TrainService:
    def __init__(self, train_repo: TrainRepository):
        self.train_repo = train_repo

    async def save_trains(self, trains: list[Train]) -> None:
        for train in trains:
            await self.train_repo.add(train)

    async def search_trains(self, from_station: str, to_station: str, date: str) -> list[Train]:
        """Search trains on the website"""
        trains = await Parser.get_trains(from_station, to_station, date)
        for train in trains:
            await self.train_repo.add(train)
        await self.train_repo.delete_expired()
        return trains

    async def search_train(self, train_id: str) -> Train | None:
        """Search and return fresh data of the train from website"""
        train_entity = await self.train_repo.get_by_id(train_id)
        if not train_entity:
            return None

        trains = await self.search_trains(train_entity.from_station, train_entity.to_station, train_entity.get_date())

        return next((train for train in (trains or []) if train.id == train_id), None)
