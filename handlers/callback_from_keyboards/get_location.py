from telebot.types import CallbackQuery, Message

from config_data.bot_messages import BotSays
from handlers.command import reset
from keyboards import choice_number_keyboard
from loader import bot, logger
from states.search_states import SearchState
from utils.decorators import exception_control
from utils.search_hotels import find_hotels_in_city


@bot.callback_query_handler(func=lambda call: call.data.endswith('key_csk'))
@exception_control.func_exception_control
def func_get_location(call: CallbackQuery) -> None:
    """
    Обработчик обратного вызова с Inline клавиатуры ключу("key_csk"), отправляет сообщение пользователю,
    сохраняет данные в data запроса, в зависимости от команды определяет дальнейшую логику выполнения запроса,
    или сбрасывает запрос если в городе не нашлось отелей.
    """

    logger.debug(f'-> INCOMING -> callback: {call.data}')

    state: str | None = bot.get_state(user_id=call.from_user.id)

    if state and state.endswith('location'):
        data_list: list = call.data.split(', ')
        city_name: str = data_list[0]
        city_id: str = data_list[1]

        hotels: dict | None = find_hotels_in_city.func_find_hotels(city_id=city_id, user_data=call)

        if hotels:
            with bot.retrieve_data(user_id=call.from_user.id) as data:
                data['location']: str = city_name
                data['city_id']: str = city_id
                data['hotels']: dict = hotels
                command: str = data['command']

            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(chat_id=call.message.chat.id, text=f"{BotSays.say('ok hotels')}<b>{city_name}</b>")

            if command == '/bestdeal':
                logger.debug(f'-> OK -> next -> ranges')
                from utils.search_hotels import ranges
                ranges.func_range(user_data=call, is_range='price')

            else:
                func_to_show_num_hotels(user_data=call)

        else:
            bot.answer_callback_query(callback_query_id=call.id)
            bot.send_message(chat_id=call.message.chat.id, text=BotSays.say('else'))
            reset.func_reset(user_data=call)

    else:
        bot.answer_callback_query(call.id, text=BotSays.old_keyboard(), show_alert=False)
        logger.debug(f'-> BAD -> keyboard does not match user state')


@exception_control.func_exception_control
def func_to_show_num_hotels(user_data: Message | CallbackQuery):
    """Отправляет пользователю клавиатуру для выбора количества отелей к показу и изменяет состояние пользователя."""
    with bot.retrieve_data(user_id=user_data.from_user.id) as data:
        hotels: dict = data['hotels']

    num_buttons = 10
    if len(hotels['results']) < 10:
        num_buttons: int = len(hotels['results'])

    keyboard = choice_number_keyboard.func_number_keyboard(num_rows=5, num_buttons=num_buttons,
                                                           key='key_snh', user_data=user_data)
    if keyboard:
        bot.send_message(chat_id=user_data.from_user.id, text=BotSays.say('question'), reply_markup=keyboard)

        bot.set_state(user_id=user_data.from_user.id, state=SearchState.show_num_hotels)

        logger.debug(f'-> OK -> next state -> show_num_hotels')
