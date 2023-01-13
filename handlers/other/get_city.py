from typing import List

from telebot.types import Message

from config_data.bot_messages import BotSays
from keyboards import city_selection_keyboard
from loader import bot, logger
from states.search_states import SearchState
from utils.decorators import exception_control
from utils.search_hotels import find_city_locations


@bot.message_handler(state=SearchState.command, content_types=['text'])
@exception_control.func_exception_control
def func_get_city(message: Message, data: dict) -> None:
    """
    Обработчик данных, введенных с клавиатуры устройства пользователя, в состоянии пользователя SearchState.command,
    логика ожидает ввода пользователем названия города для поиска отелей в нём.
    """
    incoming_city: str = message.text

    if all(map(lambda sym: sym.isalpha() or sym.isspace() or sym == '-', message.text)):
        found_cities: List[dict] | None = find_city_locations.func_find_location(incoming_city=incoming_city,
                                                                                 user_data=message)
        if found_cities:
            keyboard = city_selection_keyboard.city_keyboard(cities=found_cities, user_data=message)

            if keyboard:
                bot.send_message(chat_id=message.chat.id, text=BotSays.say('question'), reply_markup=keyboard)
                bot.set_state(user_id=message.from_user.id, state=SearchState.location)
                logger.debug(f'-> OK -> next -> callback location')

        else:
            bot.send_message(chat_id=message.from_user.id, text=BotSays.say('cities is False'))
            logger.warning(f'-> BAD -> incoming_city: {incoming_city} -> not found')

    elif incoming_city.isdigit():
        bot.send_message(chat_id=message.chat.id, text=BotSays.say('city isdigit'))

    else:
        bot.send_message(chat_id=message.chat.id, text=BotSays.say('city is rubbish'))
