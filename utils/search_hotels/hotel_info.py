from telebot.types import Message, CallbackQuery

from loader import logger, bot
from utils.decorators import exception_control
from utils.misc import usd_rate


@exception_control.func_exception_control
def func_hotel_info(hotel: dict, user_data: CallbackQuery | Message) -> str:
    """Формирует и возвращает сообщение для пользователя с информацией об отеле(hotel) по доступным данным"""

    line: str = f'<b>\n{"*" * 45}\n\nℹ️    Информация об отеле    ℹ️\nРейтинг отеля: </b>'
    url_hotel: str = f'https://www.hotels.com/ho{hotel["id"]}\n'

    try:
        hotel_stars: str = '\u2B50' * int(hotel["starRating"] // 1)
        if hotel_stars:
            line += f'{hotel_stars}\nПосмотреть отель &#128073 <a href="{url_hotel}"><b>{hotel["name"]}</b></a>\n'
        else:
            line += f'рейтинг не указан \nПосмотреть отель &#128073 <a href="{url_hotel}"><b>{hotel["name"]}</b></a>\n'
    except KeyError:
        line += f'Посмотреть отель <a href="{url_hotel}"><b>"{hotel["name"]}"</b></a>\n'

    try:
        line += f'<u>Страна</u>: {hotel["address"]["countryName"]}\n'
        line += f'<u>Местоположение</u>: {hotel["address"]["locality"]}\n'
        line += f'<u>Улица</u>: {hotel["address"]["streetAddress"]}\n'
    except KeyError:
        line += 'точный адрес не найден\n'

    try:
        lon: float = hotel["coordinate"]["lon"]
        lat: float = hotel["coordinate"]["lat"]
        url_hotel_on_map: str = f'https://yandex.ru/maps/?ll={lon}%2C{lat}&mode=search' \
                                f'&sll={lon}%2C{lat}&text={lat}%2C{lon}&z=11'
        line += f'<a href="{url_hotel_on_map}">\n🌍  Посмотреть на карте</a>\n\n' \
                f'<b>Расстояние до центра и главной достопримечательности</b>\n'
    except KeyError:
        line += f'\n\n<b>Расстояние до центра и главной достопримечательности</b>\n'

    try:
        for label in hotel['landmarks']:
            line += f'{label["label"]} - <b>{round((float(label["distance"].split()[0]) * 1.60934), 2)}</b> км\n'
    except KeyError:
        line += f'Расстояние до центра: неизвестно\n\n'

    try:
        price_USD = hotel["ratePlan"]["price"]["exactCurrent"]
        rate = usd_rate.func_rate(user_data=user_data)

        if price_USD and rate.rate_USD:
            price_RUB = int(rate.rate_USD * price_USD)
            line += f'<b>\nСтоимости</b><i> по курсу ЦБ РФ на {rate.date_rate}</i>' \
                    f'\n- в сутки:   <b>{price_RUB} </b>руб.\n'

            with bot.retrieve_data(user_id=user_data.from_user.id) as data:
                num_days = data['num_days']
            if num_days > 1:
                line += f'- за <b>{num_days}</b> суток:   <b>{price_RUB * num_days} </b>руб.\n'

    except KeyError:
        line += 'Стоимость:   <b>по запросу</b>\n'

    logger.debug(f'-> OK -> return -> line hotel info')
    return line
