from telebot.types import Message

from config_data.bot_messages import BotSays
from handlers import command
from loader import bot, logger
from utils.decorators import exception_control


@bot.message_handler(func=lambda message: True, content_types=['text'])
@exception_control.func_exception_control
def func_any_text(message: Message, data: dict) -> None:
    """
    Обработчик не распознанных текстовых данных, введенных с клавиатуры устройства пользователя, в любом состоянии
    пользователя, для реакции бота на сообщения.
    """
    logger.debug(f'-> INCOMING -> {message.text}')

    if message.text.lower() in ('help', 'sos', 'помогите', 'спасите', 'нужна помощь', 'что делать'):
        command.help.func_help(message=message, data=data)
        logger.debug(f'-> OK -> next -> help handler')

    if message.text in ('/my_id', 'my_id', 'id'):
        bot.send_message(chat_id=message.chat.id, text=f'Твой id: {message.from_user.id}')
        logger.debug(f'-> OK -> message to user -> user_id')

    else:
        bot.send_message(chat_id=message.chat.id, text=BotSays.say())
        logger.debug(f'-> BAD -> user command not identified')

