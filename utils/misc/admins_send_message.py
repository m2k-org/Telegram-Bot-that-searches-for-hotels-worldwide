import inspect
from os.path import basename

from config_data.config import ADMINS
from loader import bot, logger


def func_admins_message(user_data=None, exc=None, message=None):
    """Отправляет сообщения об ошибках и состоянии бота администраторам, если их id указаны в ADMINS."""
    try:
        if ADMINS:
            list_admins = list(map(int, ADMINS.split(', ')))
            if exc:
                if len(inspect.trace()) > 1:
                    track = inspect.trace()[1]
                else:
                    track = inspect.trace()[0]

                file = basename(track.filename)
                func = track.function
                line = track.lineno
                code = "".join(track.code_context)
                logger.error(f'-> ERROR -> User_name: {user_data.from_user.first_name}, '
                             f'User_id: {user_data.from_user.id} -> File: {file} -> Func: {func} -> Line: {line} -> '
                             f'Exception: {exc.__class__.__name__} -> Traceback: {exc} -> Code: {code.strip()}')

                for admin in list_admins:
                    bot.send_message(chat_id=admin, text='&#9888 <b><i>ERROR</i></b> &#9888\n'
                                                         f'<b>User_name</b>:    {user_data.from_user.first_name}\n'
                                                         f'<b>User_id</b>:    {user_data.from_user.id}\n'
                                                         f'<b>File</b>:    <i>{file}</i>\n'
                                                         f'<b>Func</b>:    <i>{func}</i>\n'
                                                         f'<b>Line</b>:    {line}\n'
                                                         f'<b>Exception</b>:    {exc.__class__.__name__}\n'
                                                         f'<b>Traceback</b>:    {exc}\n'
                                                         f'<b>Code</b>:    {code.strip()}\n')

                    logger.info(f'-> ADMIN SEND MESSAGE -> ERROR -> admin_id: {admin}')

            elif message:
                for admin in list_admins:
                    bot.send_message(chat_id=admin, text=message)
                    logger.info(f'-> ADMIN SEND MESSAGE -> admin_id: {admin}')

    except BaseException as exc:
        logger.exception(exc)
