import asyncio
import logging

from bot.notifier import TelegramNotifier
from domain.models.subscription import Subscription
from domain.models.train import Train
from repository.subscriptions_repository import SubscriptionsRepository
from services.booking_service import BookingService
from services.train_service import TrainService

logger = logging.getLogger(__name__)


def _check_count_seats(train: Train) -> int:
    """Return the number of available seats."""
    count = 0
    for tariff in train.tariffs.tariff_list:
        count += int(tariff['places'])
    return count


class SubscriptionMonitorService:
    def __init__(
            self,
            subscriptions_repo: SubscriptionsRepository,
            train_service: TrainService,
            booking_service: BookingService,
            notifier: TelegramNotifier,
            request_delay_seconds: float = 3.0,  # delay between requests
            check_interval_seconds: int = 300,  # delay between circle
    ):
        self.subscriptions_repo = subscriptions_repo
        self.train_service = train_service
        self.booking_service = booking_service
        self.notifier = notifier
        self.request_delay = request_delay_seconds
        self.check_interval = check_interval_seconds
        self._is_running = False

    async def start(self) -> None:
        """Starting an infinite background monitoring loop."""
        self._is_running = True
        logger.info("Background monitoring loop started.")

        while self._is_running:
            try:
                await self._process_all_subscriptions()
            except Exception as e:
                logger.error(f"Error during monitoring cycle: {e}", exc_info=True)

            await asyncio.sleep(self.check_interval)

    def stop(self) -> None:
        self._is_running = False

    async def _process_all_subscriptions(self) -> None:
        subscriptions : list[Subscription] = await self.subscriptions_repo.get_all()
        if not subscriptions:
            return

        logger.info(f"Start check subscriptions. Amount of subscriptions: {len(subscriptions)}")

        for sub in subscriptions:
            if not self._is_running:
                break

            try:
                train = await self.train_service.search_train(sub.train_id)

                if train and _check_count_seats(train) > 0:
                    logger.info(f"Found seats for train: {train}. Seats: {_check_count_seats(train)}")
                    await self.notifier.notify_free_seat(sub.user_id, train)
                    await self._handle_seats_found(sub, train)

            except Exception as e:
                logger.error(f"Error during check subscription: {sub}: {e}")


            await asyncio.sleep(self.request_delay)


    async def _handle_seats_found(self, sub: Subscription, train) -> None:
        """Logic for detecting available seats."""
        await self.booking_service.process_booking(sub)
        await self.notifier.notify_book(sub.user_id, train)
