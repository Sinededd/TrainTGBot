from aiogram.types import Message, ReplyKeyboardMarkup

from bot.states.auth_states import StateUI, STATES_PERSONAL_LIST


async def send_state_ui(message: Message, state_name: StateUI, hide_previous_message: bool = False) -> None:
    """Find state and send it to the user"""
    step: StateUI | None = next((obj for obj in STATES_PERSONAL_LIST if obj.state_name == state_name), None)

    if step is None:
        return

    if hide_previous_message:
        await message.delete()
        await message.answer(text="Данные скрыты")

    await message.answer(
        text=step.state_question,
        reply_markup=ReplyKeyboardMarkup(
            keyboard=step.keyboard_buttons,
            resize_keyboard=True,
        ),
    )