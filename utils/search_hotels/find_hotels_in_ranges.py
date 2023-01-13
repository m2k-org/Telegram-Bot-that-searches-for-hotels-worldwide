from utils.misc.usd_rate import func_rate
from loader import bot, logger
from utils.decorators import exception_control


@exception_control.func_exception_control
def find_in_ranges(user_data):
    """
    Проверяет каждый отель из списка отелей на соответствие диапазонам цен и расстояний, в случае несоответствия
    отель удаляется из списка, если после проверки список окажется пустым, выводится сообщение
    пользователю и запрос сбрасывается.
    """

    with bot.retrieve_data(user_id=user_data.from_user.id) as data:
        range_distance = data['range_distance']
        range_price = data['range_price']
        hotels = data['hotels']

    new_hotels = {'results': hotels['results'][:]}

    for hotel in hotels['results']:
        try:
            rate = func_rate(user_data=user_data)
            price = hotel["ratePlan"]["price"]["exactCurrent"] * rate.rate_USD

            if range_price.i_from > price or price > range_price.i_to:
                new_hotels['results'].remove(hotel)

            else:
                for label in hotel['landmarks']:
                    if label['label'] == 'City center':
                        distance = float(label['distance'].split()[0]) * 1.60934
                        if distance < range_distance.i_from or distance > range_distance.i_to:
                            new_hotels['results'].remove(hotel)
        except KeyError:
            new_hotels['results'].remove(hotel)

    if not len(new_hotels['results']):

        logger.debug(f'-> BAD -> return False')
        return False

    else:
        with bot.retrieve_data(user_id=user_data.from_user.id) as data:
            data['hotels'] = new_hotels

        logger.debug(f'-> OK -> return True')
        return True
