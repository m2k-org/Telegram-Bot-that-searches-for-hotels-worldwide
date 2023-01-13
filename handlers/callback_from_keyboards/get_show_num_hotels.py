from telebot.types import CallbackQuery

from config_data.bot_messages import BotSays
from keyboards import yes_no_keyboard
from loader import bot, logger
from states.search_states import SearchState
from utils.decorators import exception_control


@bot.callback_query_handler(func=lambda call: call.data.endswith('key_snh'))
@exception_control.func_exception_control
def func_get_num_hotels(call: CallbackQuery) -> None:
    """
    Обработчик обратного вызова с Inline клавиатуры по ключу("key_snh"), отправляет сообщение пользователю в
    зависимости от нажатой кнопки(callback), сохраняет данные в базу данных и изменяет состояние пользователя.
    """
    logger.debug(f'-> INCOMING -> callback: {call.data}')

    state: str | None = bot.get_state(user_id=call.from_user.id)

    if state and state.endswith('show_num_hotels'):

        data_list: list = call.data.split(', ')
        show_num_hotels: str = data_list[0]

        with bot.retrieve_data(user_id=call.from_user.id) as data:
            data['show_num_hotels'] = int(show_num_hotels)

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id, text=f"{BotSays.say('ok state')}<b>{show_num_hotels}</b>")

        keyboard = yes_no_keyboard.func_keyboard(user_data=call)
        if keyboard:
            bot.send_message(chat_id=call.message.chat.id, text=BotSays.say('question'), reply_markup=keyboard)

            bot.set_state(user_id=call.from_user.id, state=SearchState.yes_no_show_photos)
            logger.debug(f'-> OK -> next state -> yes_no_show_photos')

    else:
        bot.answer_callback_query(call.id, text=BotSays.old_keyboard(), show_alert=False)
        logger.debug(f'-> BAD -> keyboard does not match user state')
