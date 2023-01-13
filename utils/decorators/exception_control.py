import functools
from typing import Callable, Any

from telebot.apihelper import ApiTelegramException
from telebot.types import CallbackQuery, Message
from loader import logger


def func_exception_control(func: Callable) -> Callable:
    """
    Декоратор, контролирует выполнение кода в функции, в случае успешного выполнения возвращает результат
    выполнения функции, в случае исключения вызывает функцию reset.func_reset для сброса состояния пользователя
    и возвращает None.
    """

    @functools.wraps(func)
    def wrapped_func(*args, **kwargs) -> Any | None:
        try:
            result = func(*args, **kwargs)
            return result

        except BaseException as exc:
            try:
                arg = [arg for arg in args if isinstance(arg, (Message, CallbackQuery))]
                if arg:
                    user_data = arg[0]
                else:
                    user_data = kwargs.get('user_data')

                if not exc.__class__ == ApiTelegramException:

                    from utils.misc import admins_send_message
                    admins_send_message.func_admins_message(user_data=user_data, exc=exc)

                    if not func.__name__ == 'func_reset':
                        from handlers.command import reset
                        reset.func_reset(user_data=user_data, error=True)
                else:
                    logger.error(f'-> ERROR -> Exception: {exc.__class__.__name__} -> Traceback: {exc} -> '
                                 f'User_name: {user_data.from_user.first_name} '
                                 f'User_id: {user_data.from_user.id}')
                return None
            except BaseException as exc:
                logger.exception(exc)

    return wrapped_func
