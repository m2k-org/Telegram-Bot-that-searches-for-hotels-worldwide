from typing import List

from telebot.types import Message, CallbackQuery

from config_data.config import URL_city, LANGUAGE, CURRENCY, LANG_ID, SITE_ID
from loader import logger
from utils.decorators import exception_control
from utils.search_hotels import find_pattern, request_api


@exception_control.func_exception_control
def func_find_location(incoming_city: str, user_data: CallbackQuery | Message) -> List[dict] | None:
    """
    Находит и возвращает список локаций(found_cities) по названию города(incoming_city) введенного пользователем,
    если запрос к API(response_from_api) успешный, а локации по шаблону(pattern) в нём не найдены возвращает None.
    """

    found_cities: list = []
    pattern: str = r'(?<="CITY_GROUP",).+?[\]]'
    querystring: dict = {"query": f'{incoming_city}', "locale": LANGUAGE, "currency": CURRENCY}
    # querystring: dict = {"q": f'{incoming_city}', "locale": LANGUAGE, "langid": LANG_ID, "siteid": LANG_ID}
    # params: {q: 'new york', locale: 'en_US', langid: '1033', siteid: '300000001'}

    response_api: str | None = request_api.func_request(url=URL_city, querystring=querystring, user_data=user_data)

    if response_api:
        found_pattern: dict | None = find_pattern.func_find_pattern(pattern=pattern, text=response_api,
                                                                    user_data=user_data)
        if found_pattern and found_pattern.get('entities'):

            for dict_data in found_pattern['entities']:
                if dict_data.get('type') == 'CITY':
                    country: str = dict_data.get('caption').split(', ')[-1]
                    found_cities.append({'country': country,
                                         'city_name': dict_data.get('name'),
                                         'destination_id': dict_data.get('destinationId')})

            logger.debug('-> OK -> return -> found_cities')
            return found_cities

    logger.warning(f'-> BAD -> return -> None')
    return None
