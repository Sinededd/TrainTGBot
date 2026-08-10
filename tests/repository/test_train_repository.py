import pytest
import pytest_asyncio
from domain.models.train import Train
from infrastructure.db.connection import init_db
from infrastructure.db.repositories.sqlite_train_repository import SQLiteTrainRepository


@pytest_asyncio.fixture
async def repo(tmp_path):
    db_path = str(tmp_path / "test_trains.db")
    await init_db(db_path)
    return SQLiteTrainRepository(db_path=db_path)

@pytest.mark.asyncio
async def test_add_and_get_train(repo: SQLiteTrainRepository):

    test_train = Train(
        train_number="859Б",
        date_="2026-12-31",
        route="Минск-Пассажирский — Пинск",
        dep_time="13:58",
        dep_station="Минск-Пассажирский",
        arr_time="18:30",
        arr_station="Пинск",
        duration="04:32",
        train_id="1_859Б_1786705080",
        tariffs=None
    )

    # Act
    await repo.add(test_train)
    saved_entity = await repo.get_by_id(test_train.id)

    # Assert
    assert saved_entity is not None
    assert saved_entity.id == test_train.id
    assert saved_entity.from_station == test_train.from_station
    assert saved_entity.to_station == test_train.to_station


@pytest.mark.asyncio
async def test_delete_expired_trains(repo: SQLiteTrainRepository):
    past_train = Train(
        train_number="801Б",
        date_="2020-01-01",
        route="Минск — Брест",
        dep_time="10:00",
        dep_station="Минск",
        arr_time="14:00",
        arr_station="Брест",
        duration="04:00",
        train_id="past_train_id",
        tariffs=None
    )

    future_train = Train(
        train_number="802Б",
        date_="2030-01-01",
        route="Минск — Брест",
        dep_time="10:00",
        dep_station="Минск",
        arr_time="14:00",
        arr_station="Брест",
        duration="04:00",
        train_id="future_train_id",
        tariffs=None
    )

    await repo.add(past_train)
    await repo.add(future_train)

    deleted_count = await repo.delete_expired()

    assert deleted_count == 1
    assert await repo.get_by_id("past_train_id") is None
    assert await repo.get_by_id("future_train_id") is not None