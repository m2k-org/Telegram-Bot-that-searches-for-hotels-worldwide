import time
from collections import namedtuple

from telebot.handler_backends import BaseMiddleware, CancelUpdate
from telebot.types import Message, CallbackQuery

from config_data.config import LIMITED_TIME
from loader import bot, logger
from utils.decorators import exception_control
from database import database_utility


class AccessControlMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()
        self.update_types = ['message', 'callback_query']

    @exception_control.func_exception_control
    def pre_process(self, update: Message | CallbackQuery, data: dict) -> CancelUpdate | None:
        """
        Проверяет права доступа пользователя к приложению записанные в базе данных, если доступ разрешен или
        пользователь не найден в базе, пропускает сообщение пользователя к дальнейшей обработке, также передаёт далее
        данные о пользователе полученные из базы данных, предварительно записав их в словарь data.
        """

        now_date = time.time()
        user: namedtuple = database_utility.select_user(user_id=update.from_user.id, user_data=update)

        if user:
            if user.access == 'denied':
                logger.debug(f'-> BAD -> user access denied -> CancelUpdate')
                return CancelUpdate()

            elif user.access == 'limited':
                if now_date - user.start_time_limited >= LIMITED_TIME:
                    from database.database_utility import update_user_access
                    update_user_access(user_data=update, user_id=update.from_user.id, access='allowed')
                else:
                    logger.debug(f'-> BAD -> user access is limited '
                                 f'for {(LIMITED_TIME - (now_date - user.start_time_limited))//1} sec -> CancelUpdate')
                    return CancelUpdate()

        else:
            if not (isinstance(update, Message) and update.text == '/start'):
                bot.send_message(chat_id=update.from_user.id, text='&#128073 /start')
                logger.debug(f'-> BAD -> the user has not activated the app -> CancelUpdate')
                return CancelUpdate()

        data['user'] = user
        logger.debug(f'-> OK -> next -> middlewares -> flood control')
        return

    def post_process(self, message, data, exception):
        pass
