from telebot.types import Message, CallbackQuery

from loader import bot, logger
from states.search_states import SearchState
from utils.decorators import exception_control
from config_data.bot_messages import BotSays


@exception_control.func_exception_control
def func_range(user_data: Message | CallbackQuery, is_range: str) -> None:
    """Устанавливает состояние соответствующее определенной установке диапазонов, отправляет сообщение пользователю."""

    if is_range == 'price':
        bot.send_message(chat_id=user_data.from_user.id, text=BotSays.say('range price'))
        bot.set_state(user_id=user_data.from_user.id, state=SearchState.range_price)
        logger.debug(f'-> OK -> next -> range price')

    elif is_range == 'distance':
        bot.send_message(chat_id=user_data.from_user.id, text=BotSays.say('range distance'))
        bot.set_state(user_id=user_data.from_user.id, state=SearchState.range_distance)
        logger.debug(f'-> OK -> next -> range distance')

