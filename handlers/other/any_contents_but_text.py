from telebot.types import Message

from config_data.bot_messages import BotSays
from loader import bot, logger
from utils.decorators import exception_control


@bot.message_handler(func=lambda message: True, content_types=['audio', 'document', 'photo', 'sticker', 'video',
                                                               'video_note', 'voice', 'location', 'contact'])
@exception_control.func_exception_control
def func_any_message(message: Message, data: dict) -> None:
    """Обработчик не текстовых данных полученных от пользователя, для реакции бота на сообщения."""

    logger.debug(f'-> INCOMING -> not text content: {message.content_type}')

    if message.content_type in ('audio', 'voice'):
        bot.send_message(chat_id=message.chat.id, text=BotSays.say('audio, voice'))

    elif message.content_type in ('document',):
        bot.send_message(chat_id=message.chat.id, text=BotSays.say('document'))

    elif message.content_type in ('video', 'video_note'):
        bot.send_message(chat_id=message.chat.id, text=BotSays.say('video'))

    elif message.content_type in ('photo',):
        bot.send_message(chat_id=message.chat.id, text=BotSays.say('photo'))

    elif message.content_type in ('sticker',):
        bot.send_message(chat_id=message.chat.id, text=BotSays.say('sticker'))

    elif message.content_type in ('location',):
        bot.send_message(chat_id=message.chat.id, text=BotSays.say('location'))

    elif message.content_type in ('contact',):
        bot.send_message(chat_id=message.chat.id, text=BotSays.say('contact'))
