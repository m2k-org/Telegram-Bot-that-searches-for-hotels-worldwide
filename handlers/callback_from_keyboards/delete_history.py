from telebot.types import CallbackQuery
from config_data.bot_messages import BotSays
from loader import bot, logger
from utils.decorators import exception_control
from database import database_utility


@bot.callback_query_handler(func=lambda call: call.data.endswith('del_hist'))
@exception_control.func_exception_control
def func_del_history(call: CallbackQuery) -> None:
    """
    Обработчик обратного вызова с Inline клавиатуры ключу("del_hist"), отправляет сообщение пользователю в
    зависимости от нажатой кнопки(callback), и сбрасывает состояние пользователя.
    """
    logger.debug(f'-> INCOMING -> callback: {call.data}')

    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    database_utility.remove_history(user_id=call.from_user.id, user_data=call)
    bot.delete_state(user_id=call.from_user.id)
    bot.send_message(chat_id=call.message.chat.id, text=f'{BotSays.say()}', parse_mode='html')

    logger.info(f'-> OK -> history deleted -> completed successfully')

