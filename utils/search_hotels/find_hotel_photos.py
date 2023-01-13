import json
import random
import re
from typing import List

from telebot.types import Message, CallbackQuery

from config_data.config import URL_hotel_photos
from loader import logger
from utils.decorators import exception_control
from utils.search_hotels import request_api


@exception_control.func_exception_control
def func_find_photos(hotel: dict, num_photos: int, user_data: CallbackQuery | Message) -> List[str] | List[None]:
    """
    Находит и возвращает список фотографий(photos) отеля(hotels), в случае исключения(KeyError) возвращает пустой список.
    """
    photos: list = []
    try:
        main_photo: str = f'{hotel["optimizedThumbUrls"]["srpDesktop"]}'
        photos.append(main_photo)

        if num_photos > 1:
            querystring: dict = {"id": hotel["id"]}
            response_api: str = request_api.func_request(url=URL_hotel_photos, querystring=querystring,
                                                         user_data=user_data)
            data: dict = json.loads(response_api)

            if data["hotelImages"]:
                logger.debug(f'OK -> incoming response_api -> data["hotelImages"]')

                for _ in range(1, num_photos):
                    photo_dict: dict = random.choice(data["hotelImages"])
                    photo: str = re.sub(r'\{size}', 'z', f'{photo_dict["baseUrl"]}?impolicy=fcrop&w=250&h=140&q=high')
                    photos.append(photo)

    except KeyError as exc:
        logger.debug(f'-> BAD -> photo not found -> EXCEPTION: {exc} -> return -> empty photos')

    else:
        logger.debug(f'-> OK -> return -> photos')

    finally:
        return photos
