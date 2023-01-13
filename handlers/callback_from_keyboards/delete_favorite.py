from telebot.types import CallbackQuery
from config_data.bot_messages import BotSays
from database import database_utility
from loader import logger, bot
from utils.decorators import exception_control


@bot.callback_query_handler(func=lambda call: call.data.endswith('del_favor'))
@exception_control.func_exception_control
def func_del_favorites(call: CallbackQuery) -> None:
    """
    Обработчик обратного вызова с Inline клавиатуры ключу("del_favor"), отправляет сообщение пользователю в
    зависимости от нажатой кнопки(callback), и сбрасывает состояние пользователя.
    """
    logger.debug(f'-> INCOMING -> callback: {call.data}')

    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    database_utility.remove_favorite(user_id=call.from_user.id, user_data=call)
    bot.delete_state(user_id=call.from_user.id)
    bot.send_message(chat_id=call.message.chat.id, text=f'{BotSays.say()}', parse_mode='html')

    logger.info(f'-> OK -> favorite deleted -> completed successfully')


