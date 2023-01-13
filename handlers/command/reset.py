from telebot.types import Message, CallbackQuery

from config_data.bot_messages import BotSays
from loader import bot, logger
from utils.decorators import exception_control


@bot.message_handler(commands=['reset'])
@exception_control.func_exception_control
def func_reset(user_data: Message | CallbackQuery, error: bool | dict = False) -> None:
    """
    Обработчик команды /reset, сбрасывает состояние пользователя, также используется как функция сброса состояния
    в случае исключения в процессе обработки запроса от пользователя.
    """
    if isinstance(error, dict):
        error = False

    logger.debug(f'-> INCOMING -> update:{type(user_data)} error: {error}')

    if isinstance(user_data, CallbackQuery):
        chat_id: int = user_data.message.chat.id
        user_id: int = user_data.from_user.id
    else:
        chat_id: int = user_data.chat.id
        user_id: int = user_data.from_user.id

    state: str | None = bot.get_state(user_id=user_id)

    if error:
        if state:
            bot.delete_state(user_id=user_id)
            bot.send_message(chat_id=chat_id, text=BotSays.say('error in state'))
            logger.debug(f'-> OK -> state reset')
        else:
            bot.send_message(chat_id=chat_id, text=BotSays.say('error state is None'))
    else:
        if state:
            bot.delete_state(user_id=user_id)
            bot.send_message(chat_id=chat_id, text=BotSays.say('not error in state'))
            logger.debug(f'-> OK -> state reset')

        else:
            bot.send_message(chat_id=chat_id, text=BotSays.say('not error state is None'))

