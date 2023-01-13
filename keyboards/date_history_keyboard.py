from typing import List

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

from loader import logger
from utils.decorators import exception_control


@exception_control.func_exception_control
def func_history_keyboard(history_dates: List[tuple[str]], user_data: CallbackQuery | Message) -> InlineKeyboardMarkup:
    """
    Создаёт и возвращает нумерованную клавиатуру по количеству строк в сохраненной истории запросов пользователя,
    в callback дата запроса и ключ для handler.
    """

    keyboard = InlineKeyboardMarkup()

    for num, search in enumerate(history_dates):
        keyboard.add(InlineKeyboardButton(text=f'Запрос №{num + 1}  от: {search[0]}',
                                          callback_data=f'{search[0]}, key_hist'))

    keyboard.add(InlineKeyboardButton(text=f'❌  ОЧИСТИТЬ ИСТОРИЮ  ❌ ',
                                      callback_data=f'del_hist'))

    logger.debug(f'-> OK -> return -> keyboard')
    return keyboard
