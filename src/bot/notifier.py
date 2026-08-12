import logging

from aiogram import Bot

from domain.models.train import Train

logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self, bot: Bot):
        self.bot = bot

    async def notify_free_seat(self, user_id: int, train: Train):
        """Send a notification when seats become available."""
        text = (
            f"Появились свободные места на поезд:\n"
            f"№{train.train_number} ({train.from_station} ➔ {train.to_station})\n"
            f"{train.date}\n"
            f"**Успейте забронировать!**"
        )
        try:
            await self.bot.send_message(chat_id=user_id, text=text, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Failed to send a notification to the user {user_id}: {e}")

    async def notify_book(self, user_id: int, train: Train) -> None:
        """Send a booking confirmation notification"""
        text = (
            f"**Забронированно место!**\n\n"
            f"🚆 **Поезд:** №{train.train_number} ({train.from_station} ➔ {train.to_station})\n"
            f"📅 **Дата:** {train.date}\n"
            f"*Успейте купить. Срок брони 20 мин!*"
        )
        try:
            await self.bot.send_message(chat_id=user_id, text=text, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Failed to send a notification to the user {user_id}: {e}")
