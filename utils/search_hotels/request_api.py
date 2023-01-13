import requests
from telebot.types import Message, CallbackQuery

from config_data.config import HEADERS
from loader import logger
from utils.decorators import exception_control
from utils.misc.admins_send_message import func_admins_message


@exception_control.func_exception_control
def func_request(url: str, querystring: dict | None,
                 user_data: CallbackQuery | Message | None, headers: dict | None = HEADERS) -> str | None:
    """
    Запрашивает данные с API сайта(url) по заголовкам(HEADERS) и ключам(querystring), если они указаны, в случае успеха
    возвращает полученное сообщение в виде строки, в противном случае возвращает None и отправляет сообщение об ошибке
    запроса администраторам.
    """
    response_api = requests.get(url=url, headers=headers, params=querystring)
    if response_api.status_code == requests.codes.ok:
        logger.debug(f'-> OK -> return -> response_api.text')
        return response_api.text

    logger.warning(f'-> BAD -> response -> status code: {response_api.status_code} -> '
                   f'text: {response_api.text} -> return -> None')
    func_admins_message(user_data=user_data, message=f'&#9888 <b>WARNING Message to admins</b> &#9888\n'
                                                     f'<b>File:</b> request_api.py\n'
                                                     f'<b>Request to URL:</b> {url}\n'
                                                     f'<b>Response API status code:</b> {response_api.status_code}\n'
                                                     f'<b>Response API text:</b> {response_api.text} -> return -> None')
    return None
