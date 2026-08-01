from aiogram.types import Message, ReplyKeyboardMarkup

from bot.states.auth_states import StateUI, STATES_LIST


async def send_state_ui(message: Message, state_name: StateUI) -> None:
    """Find state and send it to the user"""
    step: StateUI | None = next((obj for obj in STATES_LIST if obj.state_name == state_name), None)

    if step is None:
        return

    await message.answer(
        text=step.state_question,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=step.keyboard_buttons,
            resize_keyboard=True,
        ),
    )