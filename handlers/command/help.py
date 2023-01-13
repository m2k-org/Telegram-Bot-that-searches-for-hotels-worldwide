from telebot.types import Message

from config_data.bot_messages import BotSays
from config_data.config import HELP
from loader import bot, logger
from utils.decorators import exception_control


@bot.message_handler(commands=['help'])
@exception_control.func_exception_control
def func_help(message: Message, data: dict) -> None:
    """ Обработчик команды(help), отправляет разъясняющее сообщение пользователю в зависимости от его состояния."""

    logger.debug(f'-> INCOMING -> command: {message.text}')
    state: str | None = bot.get_state(user_id=message.from_user.id)

    if state is None:
        text = [f'{command} {desk}' for command, desk in HELP]
        bot.send_message(chat_id=message.chat.id,
                         text=BotSays.say('state is None') + "\n".join(text) + BotSays.say('note'), parse_mode='html')

    elif state.endswith('command'):
        bot.send_message(chat_id=message.chat.id, text=BotSays.say('command'))

    elif state.endswith('location'):
        bot.send_message(chat_id=message.chat.id, text=BotSays.say('location'))

    elif state.endswith('show_num_hotels'):
        bot.send_message(chat_id=message.chat.id, text=BotSays.say('show_num_hotels'))

    elif state.endswith('yes_no_show_photos'):
        bot.send_message(chat_id=message.chat.id, text=BotSays.say('yes_no_show_photos'))

    elif state.endswith('show_num_photos_hotel'):
        bot.send_message(chat_id=message.chat.id, text=BotSays.say('show_num_photos_hotel'))

    elif state.endswith('travel_calendar'):
        bot.send_message(chat_id=message.chat.id, text=BotSays.say('travel_calendar'))

    elif state.endswith('history'):
        bot.send_message(chat_id=message.chat.id, text=BotSays.say('history'))

    elif state.endswith('favorites'):
        bot.send_message(chat_id=message.chat.id, text=BotSays.say('favorites'))

    elif state.endswith('range_price'):
        bot.send_message(chat_id=message.chat.id, text=BotSays.say('range_price'))

    elif state.endswith('range_distance'):
        bot.send_message(chat_id=message.chat.id, text=BotSays.say('range_distance'))

