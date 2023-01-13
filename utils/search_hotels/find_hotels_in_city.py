from telebot.types import CallbackQuery, Message

from config_data.config import URL_hotels
from loader import logger
from utils.decorators import exception_control
from utils.search_hotels import find_pattern, request_api


@exception_control.func_exception_control
def func_find_hotels(city_id: str, user_data: CallbackQuery | Message) -> dict | None:
    """Находит и возвращает отели(hotels) в городе(city_id) или None"""

    querystring: dict = {"destinationId": city_id}
    pattern: str = r'(?<=,)"results":.+?(?=,"pagination")'

    response_api: str | None = request_api.func_request(url=URL_hotels, querystring=querystring, user_data=user_data)

    if response_api:
        hotels: dict | None = find_pattern.func_find_pattern(pattern=pattern, text=response_api, user_data=user_data)

        if hotels:
            logger.debug(f'-> OK -> found hotels in response_api -> return hotels')
            return hotels

    logger.warning(f'-> BAD -> hotels not found -> return -> None')
    return None
