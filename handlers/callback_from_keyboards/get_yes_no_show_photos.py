from telebot.types import CallbackQuery

from config_data.bot_messages import BotSays
from keyboards import choice_number_keyboard
from loader import bot, logger
from states.search_states import SearchState
from utils.decorators import exception_control


@bot.callback_query_handler(func=lambda call: call.data.endswith('key_yn'))
@exception_control.func_exception_control
def func_get_yes_no_photos(call: CallbackQuery) -> None:
    """
    Обработчик обратного вызова с Inline клавиатуры ключу("key_yn"), отправляет сообщение пользователю в
    зависимости от нажатой кнопки(callback), сохраняет данные в базу данных и изменяет состояние пользователя.
    """

    logger.debug(f'-> INCOMING -> callback: {call.data}')
    state: str | None = bot.get_state(user_id=call.from_user.id)

    if state.endswith('yes_no_show_photos'):

        data_list: list = call.data.split(', ')
        show_photos: str = data_list[0]

        if state and show_photos == 'yes':
            keyboard = choice_number_keyboard.func_number_keyboard(num_rows=5, num_buttons=10,
                                                                   key='key_sph', user_data=call)
            if keyboard:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id,
                                 text=BotSays.say('yes show photos'), reply_markup=keyboard)

                bot.set_state(user_id=call.from_user.id, state=SearchState.show_num_photos_hotel)

                logger.debug(f'-> OK -> next state -> show_num_photos_hotel')

        elif show_photos == 'no':

            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            bot.send_message(chat_id=call.message.chat.id, text=BotSays.say('no show photos'))

            with bot.retrieve_data(user_id=call.from_user.id, chat_id=call.message.chat.id) as data:
                data['show_num_photos_hotel'] = 0

            bot.set_state(user_id=call.from_user.id, state=SearchState.travel_calendar)

            logger.debug(f'-> OK -> next state -> travel_calendar')

            from . import get_calendar
            get_calendar.func_calendar(user_data=call)

    else:
        bot.answer_callback_query(call.id, text=BotSays.old_keyboard(), show_alert=False)
        logger.debug(f'-> BAD -> keyboard does not match user state')
