from collections import namedtuple

from telebot.handler_backends import BaseMiddleware, CancelUpdate
from telebot.types import Message, CallbackQuery

from config_data.bot_messages import BotSays
from loader import bot, logger
from utils.decorators import exception_control


class StateControlMiddleware(BaseMiddleware):
    def __init__(self) -> None:
        super().__init__()
        self.update_types = ['message', 'callback_query']

    @exception_control.func_exception_control
    def pre_process(self, update: Message | CallbackQuery, data: dict) -> CancelUpdate | None:
        """
        Контролирует соответствие сообщений от пользователя его состоянию, в случае не соответствия
        отправляет пользователю сообщение и сбрасывает дальнейшую обработку сообщения.
        """

        state: str | None = bot.get_state(user_id=update.from_user.id)
        user: namedtuple = data.get('user')

        if user:
            if isinstance(update, Message):
                if state and update.text in ['/start', '/lowprice', '/highprice', '/bestdeal', '/history', '/favorites']:
                    bot.send_message(chat_id=update.chat.id, text=BotSays.say())
                    logger.debug(f'-> BAD -> the user did not complete the previous request -> CancelUpdate')
                    return CancelUpdate()

            elif isinstance(update, CallbackQuery):
                if state is None:
                    bot.answer_callback_query(update.id, text=BotSays.old_keyboard(), show_alert=False)
                    logger.debug(f'-> BAD -> keyboard does not match user state -> CancelUpdate')
                    return CancelUpdate()

        bot.send_chat_action(chat_id=update.from_user.id, action='typing', timeout=5)
        import handlers

    def post_process(self, message, data, exception):
        pass
