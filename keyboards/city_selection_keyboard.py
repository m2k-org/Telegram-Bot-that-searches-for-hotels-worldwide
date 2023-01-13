from typing import List

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

from loader import logger
from utils.decorators import exception_control


@exception_control.func_exception_control
def city_keyboard(cities: List[dict], user_data: Message | CallbackQuery) -> InlineKeyboardMarkup:
    """
    Создаёт и возвращает клавиатуру по количеству городов в списке(cities), в callback название города, его id и
    ключ для фильтра callback_query_handler, в названии города установленно ограничение по длине текста, чтобы не
    превышать максимально допустимый размер callback в inline кнопке в 64 байта.
    """

    keyboard = InlineKeyboardMarkup()
    for city in cities:
        keyboard.add(InlineKeyboardButton(text=f'{city.get("city_name")}, {city.get("country")}',
                                          callback_data=f'{city.get("city_name")[:21]}, {city.get("destination_id")}, '
                                                        f'key_csk'))
    logger.debug(f'-> OK -> return -> keyboard')
    return keyboard
