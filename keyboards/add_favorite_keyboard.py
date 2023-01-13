from typing import List

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import logger
from utils.decorators import exception_control


@exception_control.func_exception_control
def func_add_favorites_keyboard(date_info: List[tuple[str]]) -> InlineKeyboardMarkup:
    """
    Создаёт и возвращает клавиатуру да/ нет, в callback дата запроса и ключ для handler.
    """

    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(InlineKeyboardButton(text='☑️  Да', callback_data=f'yes, {date_info}, fav'),
                 InlineKeyboardButton(text='❌  Нет', callback_data=f'no, {date_info}, fav'))

    logger.debug(f'-> OK -> return -> keyboard')
    return keyboard

