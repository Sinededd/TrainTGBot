import logging

from domain.models.user import User
from repository.user_repository import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def upsert_user(self, user: User) -> bool:
        """Register a new user
        Returns True if registration was successful, False if user already exists"""
        existing_user = await self.user_repo.get_by_id(user.id)
        if existing_user:
            await self.user_repo.add(user)  # Update existing user
            logging.info(f"User {user.id} was updated.")
            return False

        logging.info(f"Creating new user: {user}")

        await self.user_repo.add(user)
        return True

    async def get_user(self, user_id: int) -> User | None:
        return await self.user_repo.get_by_id(user_id)
