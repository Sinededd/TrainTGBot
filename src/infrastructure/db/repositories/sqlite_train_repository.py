from infrastructure.db.connection import DEFAULT_DB_PATH, get_db
from domain.dto.train_entity import TrainEntity
from domain.dto.train_mapper import TrainMapper
from domain.models.train import Train
from repository.train_repository import TrainRepository


class SQLiteTrainRepository(TrainRepository):
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path

    async def get_by_id(self, train_id: str) -> TrainEntity | None:
        async with get_db(self.db_path) as db:
            async with db.execute(
                    """
                    SELECT id, train_number, from_station, to_station, departure_datetime
                    FROM trains WHERE id = ?
                    """,
                    (train_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return TrainEntity(
                        train_id=row[0], train_number=row[1], from_station=row[2], to_station=row[3], departure_datetime=row[4]
                    )
                return None

    async def add(self, train: Train) -> None:
        train_entity = TrainMapper.to_train_entity(train)
        async with get_db(self.db_path) as db:
            await db.execute(
                """
                INSERT OR IGNORE INTO trains (id, train_number, from_station, to_station, departure_datetime)
                VALUES (?, ?, ?, ?, ?)
                """,
                (train_entity.id, train_entity.train_number, train_entity.from_station, train_entity.to_station, train_entity.departure_datetime)
            )
            await db.commit()

    async def delete_expired(self) -> int:
        async with get_db(self.db_path) as db:
            cursor = await db.execute(
                "DELETE FROM trains WHERE datetime(departure_datetime) < datetime('now', 'localtime')"
            )
            await db.commit()
            return cursor.rowcount
