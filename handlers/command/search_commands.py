from telebot.types import Message

from config_data.bot_messages import BotSays
from loader import bot, logger
from states.search_states import SearchState
from utils.decorators import exception_control


@bot.message_handler(commands=['lowprice', 'highprice', 'bestdeal'])
@exception_control.func_exception_control
def func_search_commands(message: Message, data: dict) -> None:
    """Обработчик команд(lowprice, highprice, bestdeal), запускает сценарий поиска и сортировки отелей."""
    logger.debug(f'-> INCOMING -> command: {message.text}')

    bot.set_state(user_id=message.from_user.id, state=SearchState.command)
    with bot.retrieve_data(user_id=message.from_user.id) as data:
        data['command']: str = message.text

    bot.send_message(chat_id=message.chat.id, text=BotSays.say())
