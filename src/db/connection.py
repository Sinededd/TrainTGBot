from contextlib import asynccontextmanager

import aiosqlite

DEFAULT_DB_PATH = "database.db"


@asynccontextmanager
async def get_db(db_path: str = DEFAULT_DB_PATH):
    """Async context manager to get database connection"""
    async with aiosqlite.connect(db_path) as db:
        await db.execute("PRAGMA foreign_keys = ON;")
        yield db


async def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    """Initialize database"""
    async with get_db(db_path) as db:
        await db.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                surname TEXT NOT NULL,
                name TEXT NOT NULL,
                patronymic TEXT NOT NULL,
                passport_number TEXT NOT NULL UNIQUE,
                login TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS trains (
                id TEXT PRIMARY KEY,
                train_number TEXT NOT NULL,
                from_station TEXT NOT NULL,
                to_station TEXT NOT NULL,
                departure_datetime TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS subscriptions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                train_id TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (train_id) REFERENCES trains(id) ON DELETE CASCADE,

                UNIQUE(user_id, train_id)
            );
        """)
        await db.commit()