from typing import List

from telebot.types import Message

from config_data.bot_messages import BotSays
from keyboards import date_favorite_keyboard
from loader import bot, logger
from states.search_states import SearchState
from utils.decorators import exception_control
from database import database_utility


@bot.message_handler(commands=['favorites'])
@exception_control.func_exception_control
def func_favorites(message: Message, data: dict) -> None:
    """
    Обработчик команды /favorites, отправляет клавиатуру с датами избранных отелей пользователя или сообщение об
    отсутствии избранных.
    """

    logger.debug(f'-> INCOMING -> command: {message.text}')
    favorites_dates: List[tuple[str]] = database_utility.select_favorites_dates(user_id=message.from_user.id,
                                                                                user_data=message)
    if favorites_dates:
        keyboard = date_favorite_keyboard.func_favorite_keyboard(favorite_dates=favorites_dates, user_data=message)

        if keyboard:
            bot.send_message(chat_id=message.chat.id, text=BotSays.say('question'), reply_markup=keyboard)
            bot.set_state(user_id=message.from_user.id, state=SearchState.favorites)
            logger.debug(f'-> OK -> message to user with search favorite date keyboard')

    else:
        bot.send_message(chat_id=message.chat.id, text=BotSays.say('no favorite'))
        logger.debug(f'-> OK -> message to user no search favorite')
