from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, Message, CallbackQuery

from loader import logger
from utils.decorators import exception_control


@exception_control.func_exception_control
def func_keyboard(user_data: CallbackQuery | Message) -> InlineKeyboardMarkup:
    """Создает и возвращает клавиатуру с двумя кнопками Да и Нет, в callback да/нет и ключ для handler."""
    keyboard = InlineKeyboardMarkup(row_width=2)

    keyboard.add(InlineKeyboardButton(text='☑️  Да', callback_data='yes, key_yn'),
                 InlineKeyboardButton(text='❌  Нет', callback_data='no, key_yn'))

    logger.debug(f'-> OK -> return keyboard')
    return keyboard



