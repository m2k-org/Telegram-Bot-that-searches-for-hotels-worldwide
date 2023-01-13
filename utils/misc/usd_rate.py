import json
import time
from collections import namedtuple

from config_data.config import RATE_UPDATE
from loader import logger
from utils.decorators import exception_control
from database import database_utility


@exception_control.func_exception_control
def func_rate(user_data):
    """
    Возвращает курс USD и дату сохраненные в базе данных, если данные устарели более чем на RATE_UPDATE,
    обновляет их, запрашивая актуальные данные на сайте URL_cbr, и возвращает обновленные курс USD и дату.
    """
    now_time = int(time.time())
    rate_USD, date_rate, time_record = 0, None, now_time

    rate_in_db = database_utility.select_rate(user_data=user_data)

    if rate_in_db and (now_time - rate_in_db.time_record) < RATE_UPDATE:
        rate_USD = rate_in_db.rate_USD
        date_rate = rate_in_db.date_rate
        time_record = rate_in_db.time_record

    else:
        from utils.search_hotels import request_api
        from config_data.config import URL_cbr

        response_api = request_api.func_request(url=URL_cbr, headers=None, querystring=None, user_data=user_data)
        if response_api:
            response_api = json.loads(response_api)
            date_rate = response_api['Date'].split('T')[0]
            date_rate = ".".join(date_rate.split('-')[::-1])
            rate_USD = response_api['Valute']['USD']['Value']
            time_record = now_time

            if not rate_in_db:
                database_utility.insert_rate(rate=rate_USD, date=date_rate, time=time_record, user_data=user_data)
            else:
                database_utility.update_rate(rate=rate_USD, date=date_rate, time=time_record, user_data=user_data)

    rate = namedtuple('rate', ['rate_USD', 'date_rate', 'time_record'])
    rate = rate(rate_USD, date_rate, time_record)
    logger.debug(f'-> OK -> return -> {rate}')
    return rate
