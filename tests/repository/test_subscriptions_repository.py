import pytest
import pytest_asyncio

from infrastructure.db.connection import init_db
from infrastructure.db.repositories.sqlite_subscriptions_repository import SQLiteSubscriptionsRepository
from infrastructure.db.repositories.sqlite_train_repository import SQLiteTrainRepository
from infrastructure.db.repositories.sqlite_user_repository import SQLiteUserRepository
from domain.models.train import Train
from domain.models.user import User


@pytest_asyncio.fixture
async def repo(tmp_path_factory):
    tmp_path = tmp_path_factory.mktemp("data")
    db_path = str(tmp_path / "test_trains.db")
    await init_db(db_path)

    train = Train(
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
    await SQLiteTrainRepository(db_path).add(train)

    user = User(
        id=123456789,
        surname="NN",
        name="MM",
        patronymic="SS",
        passport_number="123123",
        login="login",
        password="password",
        created_at=None
    )
    await SQLiteUserRepository(db_path).add(user)

    return SQLiteSubscriptionsRepository(db_path=db_path)


@pytest.fixture
def user_id():
    return 123456789


@pytest.fixture
def train_id():
    return "1_859Б_1786705080"


@pytest.mark.asyncio
async def test_add_and_check_subscription(repo: SQLiteSubscriptionsRepository, user_id: int, train_id: str):
    """Test adding and checking subscription existence"""
    await repo.add(user_id=user_id, train_id=train_id)
    assert await repo.check(user_id=user_id, train_id=train_id) is True


@pytest.mark.asyncio
async def test_add_and_delete_subscription(repo: SQLiteSubscriptionsRepository, user_id: int, train_id: str):
    """Test removing subscription"""
    await repo.add(user_id=user_id, train_id=train_id)
    await repo.remove(user_id=user_id, train_id=train_id)
    assert await repo.check(user_id=user_id, train_id=train_id) is False


@pytest.mark.asyncio
async def test_add_and_get_subscription(repo: SQLiteSubscriptionsRepository, user_id: int, train_id: str):
    """Test getting subscriptions by user and by train"""
    await repo.add(user_id=user_id, train_id=train_id)

    trains = await repo.get_all_by_user_id(user_id=user_id)
    assert len(trains) == 1
    assert trains[0] == (train_id,)

    users = await repo.get_all_by_train_id(train_id=train_id)
    assert len(users) == 1
    assert users[0] == (user_id,)


@pytest.mark.asyncio
async def test_add_duplicate_subscription(repo: SQLiteSubscriptionsRepository, user_id: int, train_id: str):
    """Test adding duplicate subscription"""
    await repo.add(user_id=user_id, train_id=train_id)
    await repo.add(user_id=user_id, train_id=train_id)

    trains = await repo.get_all_by_user_id(user_id=user_id)
    assert len(trains) == 1
    assert trains[0] == (train_id,)


@pytest.mark.asyncio
async def test_get_subscriptions_for_nonexistent_user(repo: SQLiteSubscriptionsRepository):
    """Test getting subscriptions for nonexistent user"""
    trains = await repo.get_all_by_user_id(user_id=999999999)
    assert len(trains) == 0


@pytest.mark.asyncio
async def test_get_users_for_nonexistent_train(repo: SQLiteSubscriptionsRepository):
    """Test getting users for nonexistent train"""
    users = await repo.get_all_by_train_id(train_id="nonexistent_train")
    assert len(users) == 0


@pytest.mark.asyncio
async def test_remove_nonexistent_subscription(repo: SQLiteSubscriptionsRepository, user_id: int, train_id: str):
    """Test removing nonexistent subscription (should not raise an error)"""
    await repo.remove(user_id=user_id, train_id=train_id)
    assert await repo.check(user_id=user_id, train_id=train_id) is False