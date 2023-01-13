from typing import List

from telebot.types import CallbackQuery, Message

from loader import logger
from utils.decorators import exception_control


def sort_price(hotel: dict) -> float:
    """Возвращает стоимость отеля, если её нет в словаре возвращает 99,99 """
    try:
        return hotel['ratePlan']['price']['exactCurrent']
    except KeyError:
        logger.debug(f'-> BAD -> not found price hotel-> return -> 99.99')
        return 99.99


def sort_city_center(hotel: dict) -> float:
    """Возвращает расстояние до центра, если его нет в словаре возвращает 99,99 """
    try:
        for landmark in hotel['landmarks']:
            if landmark['label'] == 'City center':
                return float(landmark['distance'].split()[0])
        else:
            return 99.99
    except KeyError:
        logger.debug(f'-> BAD -> not found distance to city center -> return -> 99.99')
        return 99.99


@exception_control.func_exception_control
def func_sort_hotels(command: str, hotels: dict, user_data: CallbackQuery | Message) -> List[dict] | None:
    """
    Сортирует отели по выбранному сценарию:
    /highprice: сначала дорогие
    /lowprice: сначала дешёвые
    /bestdeal: двойная сортировка дешевые отели ближе всего к центру
    """
    if command == '/highprice':
        reverse = True
    else:
        reverse = False

    hotels: List[dict] = sorted(hotels['results'], key=lambda hotel: sort_price(hotel), reverse=reverse)

    if command == '/bestdeal':
        hotels: List[dict] = sorted(hotels, key=lambda hotel: sort_city_center(hotel))

    logger.debug(f'-> OK -> return sorted hotels by command: {command}')
    return hotels
