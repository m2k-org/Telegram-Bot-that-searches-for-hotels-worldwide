from telebot.types import Message

from config_data.bot_messages import BotSays
from loader import bot, logger
from utils.decorators import exception_control
from database import database_utility


@bot.message_handler(commands=['start'])
@exception_control.func_exception_control
def start(message: Message, data: dict) -> None:
    """
    Обработчик команды /start от пользователя, если пользователь не найден в базе данных, записывает его, таким образом
    запускает процесс взаимодействия бота с пользователем, а если он найден, отправляет пользователю сообщение
    -> бот уже запущен.
    """
    logger.debug(f'-> INCOMING -> command: {message.text}')

    user = data['user']
    if user:
        bot.send_message(chat_id=message.chat.id,
                         text=f"<b>{message.from_user.full_name}</b> 😄️! {BotSays.say('user')}", parse_mode='html')

    else:
        database_utility.insert_user(user_data=message, user_id=message.from_user.id, name=message.from_user.full_name,
                                     access='allowed')

        bot.send_message(chat_id=message.chat.id,
                         text=f"😄️ Привет, {message.from_user.full_name}!\n{BotSays.say('not user')}")

        logger.info(f'-> NEW USER -> name: {message.from_user.full_name} , id: {message.from_user.id}')
