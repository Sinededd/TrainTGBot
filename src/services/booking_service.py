import logging

from playwright.async_api import Browser

from infrastructure.crypto import decrypt_text
from infrastructure.parser import seats_extractor
from infrastructure.parser.rw_parser import Parser
from models.subscription import Subscription
from repository.train_repository import TrainRepository
from services.user_service import UserService

logger = logging.getLogger(__name__)


class BookingService:
    def __init__(self, train_repository: TrainRepository, user_service: UserService, browser: Browser):
        self.train_repository = train_repository
        self.user_service = user_service
        self.browser = browser

    async def process_booking(self, subscription: Subscription) -> None:
        context = await self.browser.new_context()
        parser = Parser(context)
        user = await self.user_service.get_user(subscription.user_id)
        if not user:
            logger.error(f"User {subscription.user_id} not found")
            return
        await parser.login(login=user.login, password=decrypt_text(user.password))

        train_entity = await self.train_repository.get_by_id(subscription.train_id)
        if not train_entity:
            logger.error(f"Train {subscription.train_id} not found")
            return

        train_data = await parser.get_train_data(
            train_number=train_entity.train_number,
            from_station=train_entity.from_station,
            to_station=train_entity.to_station,
            date=train_entity.get_date(),
            time_=train_entity.get_time(),
        )
        seats = seats_extractor.extract_seats(train_data)
        seat = seats.get_first()

        if seat:
            await parser.choose_train(
                train_id=train_entity.id,
                from_station=train_entity.from_station,
                to_station=train_entity.to_station,
                date=train_entity.get_date(),
            )
            await parser.choose_seat(seat)
            await parser.place_an_order(
                surname=user.surname,
                name=user.name,
                patronymic=user.patronymic,
                passNumber=decrypt_text(user.passport_number),
            )

        await context.close()
