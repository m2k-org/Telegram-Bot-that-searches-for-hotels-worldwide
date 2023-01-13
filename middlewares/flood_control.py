import time

from telebot.handler_backends import BaseMiddleware, CancelUpdate
from telebot.types import Message, CallbackQuery

from config_data.bot_messages import BotSays
from loader import bot, logger
from utils.decorators import exception_control
from config_data.config import ANTIFLOOD_TIME, LIMITED_TIME


class FloodControlMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()
        self.__last_users_updates = {}
        self.update_types = ['message', 'callback_query']

    @exception_control.func_exception_control
    def pre_process(self, update: Message | CallbackQuery, data: dict) -> CancelUpdate | None:
        """Контролирует время между сообщениями от пользователя для защиты от "флуда"."""

        now_date = time.time()

        if not update.from_user.id in self.__last_users_updates:
            self.__last_users_updates[update.from_user.id] = now_date, 0
            logger.debug(f'-> OK -> next -> middlewares -> state and user control')
            return

        else:
            user_id = update.from_user.id
            time_last_update = self.__last_users_updates[update.from_user.id][0]
            num_flood = self.__last_users_updates[update.from_user.id][1]

            if now_date - time_last_update < ANTIFLOOD_TIME:
                if (isinstance(update, CallbackQuery) and num_flood > 3) \
                        or (isinstance(update, Message) and num_flood > 10):

                    from database.database_utility import update_user_access
                    update_user_access(user_data=update, user_id=update.from_user.id,
                                       access='limited', start_time_limited=now_date)

                    bot.send_message(chat_id=user_id,
                                     text=BotSays.say('lot flooding') + f'{LIMITED_TIME // 60} мин')
                    del self.__last_users_updates[user_id]
                    return CancelUpdate()

                else:
                    if isinstance(update, Message):
                        bot.delete_message(chat_id=update.chat.id, message_id=update.id)
                        if num_flood == 0:
                            bot.send_message(chat_id=update.chat.id, text=BotSays.say('too fast'))
                        logger.debug(f'-> BAD -> user is flooding -> CancelUpdate')

                    elif isinstance(update, CallbackQuery):
                        bot.answer_callback_query(callback_query_id=update.id)
                        logger.debug(f'-> BAD -> user is flooding the keyboard-> CancelUpdate')

                    self.__last_users_updates[user_id] = now_date, num_flood + 1
                    return CancelUpdate()

            else:
                self.__last_users_updates[user_id] = now_date, 0
                logger.debug(f'-> OK -> next -> middlewares -> state and user control')
                return

    def post_process(self, message, data, exception):
        pass
