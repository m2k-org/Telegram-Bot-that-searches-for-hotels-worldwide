from typing import List

from telebot.types import CallbackQuery

from config_data.bot_messages import BotSays
from loader import bot
from utils.decorators import exception_control
from keyboards import add_favorite_keyboard
from states.search_states import SearchState


@exception_control.func_exception_control
def func_add_favorites(date: List[tuple[str]], call: CallbackQuery) -> None:
    """
    Предлагает пользователю добавить историю поиска в избранное и записывает результат поиска отелей в базу
    данных.
    """

    keyboard = add_favorite_keyboard.func_add_favorites_keyboard(date_info=date)

    if keyboard:
        bot.send_message(chat_id=call.message.chat.id, text=f"{BotSays.say('question')}",
                         reply_markup=keyboard)
        bot.set_state(user_id=call.message.from_user.id, state=SearchState.favorites)

