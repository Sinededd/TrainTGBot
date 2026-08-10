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