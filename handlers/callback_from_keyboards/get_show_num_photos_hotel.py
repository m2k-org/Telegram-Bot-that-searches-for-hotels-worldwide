from telebot.types import CallbackQuery

from config_data.bot_messages import BotSays
from loader import bot, logger
from states.search_states import SearchState
from utils.decorators import exception_control
from . import get_calendar


@bot.callback_query_handler(func=lambda call: call.data.endswith('key_sph'))
@exception_control.func_exception_control
def func_get_num_photos(call: CallbackQuery) -> None:
    """
    Обработчик обратного вызова с Inline клавиатуры по ключу("key_sph"), отправляет сообщение пользователю в
    зависимости от нажатой кнопки(callback), изменяет состояние пользователя.
    """

    logger.debug(f'-> INCOMING -> callback: {call.data}')
    state: str | None = bot.get_state(user_id=call.from_user.id)

    if state and state.endswith('show_num_photos_hotel'):

        data_list: list = call.data.split(', ')
        show_photos: str = data_list[0]

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id, text=f'{BotSays.say()}<b>{show_photos}</b>')

        with bot.retrieve_data(user_id=call.from_user.id) as data:
            data['show_num_photos_hotel'] = int(show_photos)

        bot.set_state(user_id=call.from_user.id, state=SearchState.travel_calendar)

        logger.debug(f'-> OK -> next state -> travel_calendar')
        get_calendar.func_calendar(user_data=call)

    else:
        bot.answer_callback_query(call.id, text=BotSays.old_keyboard(), show_alert=False)
        logger.debug(f'-> BAD -> keyboard does not match user state')
