from typing import List

from telebot.types import Message

from config_data.bot_messages import BotSays
from keyboards import date_history_keyboard
from loader import bot, logger
from states.search_states import SearchState
from utils.decorators import exception_control
from database import database_utility


@bot.message_handler(commands=['history'])
@exception_control.func_exception_control
def func_history(message: Message, data: dict) -> None:
    """
    Обработчик команды /history, отправляет клавиатуру с датами истории поиска пользователя или сообщение об отсутствии
    истории поиска.
    """

    logger.debug(f'-> INCOMING -> command: {message.text}')
    history_dates: List[tuple[str]] = database_utility.select_history_dates(user_id=message.from_user.id,
                                                                            user_data=message)
    if history_dates:
        keyboard = date_history_keyboard.func_history_keyboard(history_dates=history_dates, user_data=message)

        if keyboard:
            bot.send_message(chat_id=message.chat.id, text=BotSays.say('question'), reply_markup=keyboard)
            bot.set_state(user_id=message.from_user.id, state=SearchState.history)
            logger.debug(f'-> OK -> message to user with search history date keyboard')

    else:
        bot.send_message(chat_id=message.chat.id, text=BotSays.say('no history'))
        logger.debug(f'-> OK -> message to user no search history')
