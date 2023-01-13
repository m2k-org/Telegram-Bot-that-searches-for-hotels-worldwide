from typing import List

from telebot.types import CallbackQuery

from config_data.bot_messages import BotSays
from database import database_utility
from loader import logger, bot
from utils.decorators import exception_control


@bot.callback_query_handler(func=lambda call: call.data.endswith('key_favor'))
@exception_control.func_exception_control
def func_get_favorite(call: CallbackQuery) -> None:
    """
    Обработчик обратного вызова с Inline клавиатуры ключу("key_favor"), отправляет сообщение пользователю в
    зависимости от нажатой кнопки(callback), и сбрасывает состояние пользователя.
    """
    logger.debug(f'-> INCOMING -> callback: {call.data}')

    state: str | None = bot.get_state(user_id=call.from_user.id)

    if state and state.endswith('favorites'):

        date: str = call.data.split(', ')[0]

        favorite: List[str] = database_utility.select_favorites(user_id=call.from_user.id, date=date, user_data=call)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.send_message(chat_id=call.message.chat.id, text=f'{favorite[0]}', disable_web_page_preview=True)

        bot.delete_state(user_id=call.from_user.id)

        logger.info(f'-> OK -> command: /favorites -> completed successfully')

    else:
        bot.answer_callback_query(call.id, text=BotSays.old_keyboard(), show_alert=False)
        logger.debug(f'-> BAD -> keyboard does not match user state')