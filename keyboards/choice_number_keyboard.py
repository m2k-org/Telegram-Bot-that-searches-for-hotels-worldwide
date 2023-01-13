from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

from loader import logger
from utils.decorators import exception_control


@exception_control.func_exception_control
def func_number_keyboard(num_rows: int, num_buttons: int, key: str,
                         user_data: CallbackQuery | Message) -> InlineKeyboardMarkup:
    """
    Создаёт и возвращает нумерованную клавиатуру, в callback название номер(button), ключ(key) для handler.
    """
    buttons: list = []
    keyboard = InlineKeyboardMarkup(row_width=num_rows)

    for button in range(1, num_buttons + 1):
        buttons.append(InlineKeyboardButton(text=button, callback_data=f'{button}, {key}'))
    keyboard.add(*buttons)

    logger.debug(f'-> OK -> return keyboard')
    return keyboard
