from telebot.types import CallbackQuery
from database import database_utility
from loader import logger, bot
from utils.decorators import exception_control
from config_data.bot_messages import BotSays


@bot.callback_query_handler(func=lambda call: call.data.endswith('fav'))
@exception_control.func_exception_control
def func_get_yes_no_favorite(call: CallbackQuery) -> None:
    """
    Обработчик обратного вызова с Inline клавиатуры ключу("fav"), отправляет сообщение пользователю в
    зависимости от нажатой кнопки(callback), сохраняет данные в базу данных и удаляет состояние пользователя.
    """

    logger.debug(f'-> INCOMING -> callback: {call.data}')

    data_list: list = call.data.split(', ')
    result: str = data_list[0]
    date = data_list[1]

    if result == 'yes':

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        database_utility.insert_favorite(user_id=call.from_user.id, date_info=date, user_data=call)
        bot.send_message(chat_id=call.message.chat.id,
                         text=f"{BotSays.say('yes')}",
                         parse_mode='html')

        logger.debug(f'-> OK -> next state -> show_num_photos_hotel')

    elif result == 'no':

        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id,
                         text=f"{BotSays.say('no')}",
                         parse_mode='html')

        logger.debug(f'-> OK -> next state -> travel_calendar')

    else:
        bot.answer_callback_query(call.id, text=BotSays.old_keyboard(), show_alert=False)
        logger.debug(f'-> BAD -> keyboard does not match user state')

    bot.delete_state(user_id=call.from_user.id)
