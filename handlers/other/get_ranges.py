from collections import namedtuple

from telebot.types import Message

from config_data.bot_messages import BotSays
from handlers.callback_from_keyboards import get_location
from loader import bot, logger
from states.search_states import SearchState
from utils.decorators import exception_control
from utils.search_hotels import ranges, find_hotels_in_ranges


@bot.message_handler(state=[SearchState.range_price, SearchState.range_distance], content_types=['text'])
@exception_control.func_exception_control
def func_get_ranges(message: Message, data: dict) -> None:
    """
    Обработчик данных, введенных с клавиатуры устройства пользователя, в состояниях пользователя
    SearchState.range_price или SearchState.range_distance, логика ожидает ввода пользователем диапазонов цен и
    расстояний в виде двух чисел через пробел для установки критериев поиска отелей.
    """

    try:
        if all(map(lambda x: x.isdigit() or x in (',', '.', ' '), message.text)) and len(message.text.split()) == 2:

            i_range = namedtuple('i_range', ['i_from', 'i_to'])
            i_range = i_range._make(float(elem) if elem.isdigit() or '.' in elem else
                                    float(elem.replace(',', '.')) if ',' in elem else
                                    None for elem in message.text.split())

            if i_range.i_to < i_range.i_from:
                bot.send_message(chat_id=message.from_user.id, text=BotSays.say('negative range'))
                logger.debug(f'-> BAD -> negative range from user')

            else:
                state: str | None = bot.get_state(user_id=message.from_user.id)

                if state.endswith('range_price'):
                    with bot.retrieve_data(user_id=message.from_user.id) as data:
                        data['range_price']: namedtuple = i_range

                    bot.send_message(chat_id=message.from_user.id,
                                     text=f'Цена за сутки:  <b>{str(i_range.i_from).rstrip("0").rstrip(".")} руб.</b>  -'
                                          f'  <b>{str(i_range.i_to).rstrip("0").rstrip(".")} руб.</b>')

                    ranges.func_range(user_data=message, is_range='distance')

                elif state.endswith('range_distance'):
                    with bot.retrieve_data(user_id=message.from_user.id) as data:
                        data['range_distance']: namedtuple = i_range
                        city = data['location']

                    bot.send_message(chat_id=message.from_user.id,
                                     text=f'Расстояние до центра:   <b>{str(i_range.i_from).rstrip("0").rstrip(".")}'
                                          f'</b> - <b>{str(i_range.i_to).rstrip("0").rstrip(".")}</b> км')

                    if find_hotels_in_ranges.find_in_ranges(user_data=message):
                        logger.debug(f'-> OK -> next -> get_location')

                        get_location.func_to_show_num_hotels(user_data=message)

                    else:
                        logger.debug(f'-> BAD -> no hotels by ranges')
                        bot.send_message(chat_id=message.from_user.id,
                                         text=f'😥 В <b>{city}</b>' + BotSays.say('not hotels'))

                        from handlers.command import reset
                        reset.func_reset(user_data=message)

        else:
            bot.send_message(chat_id=message.from_user.id, text=BotSays.say('not numbers'))
            logger.debug(f'-> BAD -> not numbers from user')

    except ValueError:
        bot.send_message(chat_id=message.from_user.id, text=BotSays.say('exception'))
        logger.debug(f'-> BAD -> many separators in numbers from user')
