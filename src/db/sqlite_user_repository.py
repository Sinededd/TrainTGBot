from typing import Sequence

from db.connection import get_db, DEFAULT_DB_PATH
from models.user import User
from repository.user_repository import UserRepository


class SQLiteUserRepository(UserRepository):
    def __init__(self, db_path: str = DEFAULT_DB_PATH):
        self.db_path = db_path

    async def add(self, user: User) -> None:
        async with get_db(self.db_path) as db:
            await db.execute(
                """
                INSERT INTO users (id, surname, name, patronymic, passport_number, login, password)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (user.id, user.surname, user.name, user.patronymic, user.passport_number, user.login, user.password)
            )
            await db.commit()

    async def get_by_id(self, user_id: int) -> User | None:
        async with get_db(self.db_path) as db:
            async with db.execute(
                    """
                    SELECT id, surname, name, patronymic, passport_number, login, password, created_at 
                    FROM users WHERE id = ?
                    """,
                    (user_id,)
            ) as cursor:
                row = await cursor.fetchone()
                if row:
                    return User(
                        id=row[0], surname=row[1], name=row[2], patronymic=row[3],
                        passport_number=row[4], login=row[5], password=row[6], created_at=row[7]
                    )
                return None

    async def list_all(self) -> Sequence[User]:
        async with get_db(self.db_path) as db:
            async with db.execute(
                    "SELECT id, surname, name, patronymic, passport_number, login, password, created_at FROM users"
            ) as cursor:
                rows = await cursor.fetchall()
                return [
                    User(
                        id=r[0], surname=r[1], name=r[2], patronymic=r[3],
                        passport_number=r[4], login=r[5], password=r[6], created_at=r[7]
                    )
                    for r in rows
                ]
