import os

from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit('Переменные окружения не загружены т.к отсутствует файл .env\n'
         'Необходимо верно заполнить данные в файле .env.template и переименовать его в .env')
else:
    load_dotenv()

# Уникальный ключ телеграмм бота -> загружается из файла .env
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Уникальный ключ  для "hotels4.p.rapidapi.com" -> загружается из файла .env
RAPID_API_KEY = os.getenv('RAPID_API_KEY')

# Параметры HTML запросов к API Нotels
HOST = "hotels4.p.rapidapi.com"
HEADERS = {"X-RapidAPI-Host": HOST, "X-RapidAPI-Key": RAPID_API_KEY}
LANGUAGE = "ru_RU"
CURRENCY = "RUB"
# LANG_ID = '1033'
# SITE_ID = '300000001'

URL = "https://" + HOST
URL_city = URL + "/locations/v2/search"
URL_hotels = URL + "/properties/v2/list"
URL_hotel_photos = URL + "/properties/get-hotel-photos"

# URL API ЦБ РФ
URL_cbr = 'https://www.cbr-xml-daily.ru/daily_json.js'

# Параметр в секундах регулярности обновления курса USD при условии запроса от пользователя
RATE_UPDATE = 10800  # 3 часа

# Команды бота (также есть команда my_id в ответ возвращает id пользователя)
DEFAULT_COMMANDS = (('start', "запустить бота"),
                    ('help', "вывести справку"),
                    ('lowprice', "топ дешёвых отелей в городе"),
                    ('highprice', "топ дорогих отелей в городе"),
                    ('bestdeal', "топ дешёвых отелей ближе к центру"),
                    ('history', "история поиска отелей"),
                    ('favorites', "избранные"),
                    ('reset', "сброс текущего запроса"),
                    )

HELP = [('<b>Поиск отелей</b>\n',
         "/lowprice - Недорогие отели, сортировка по возрастанию цены ⏫\n"
         "/highprice - Дорогие отели, сортировка по убыванию цены ⏬\n"
         "/bestdeal - Поиск отеля с условиями: диапазон цен, удаленность от центра \n"),
        ('<b>История поиска</b>\n', "/history - История поиска. Найденные отели и вызванные команды \n"),
        ('<b>Стандартные команды</b>\n',
         "/start - Перезапускает работу бота ↩\n"
         "/help - Выводит данное сообщение 🆘\n"),
        ('<b>Рекомендации</b>\n',
         "При возникших ошибках:\n"
         "1. Попробуйте перезапустить бота, отправив боту /start ↩\n"
         "2. Иногда на сервере возникают ошибки, не зависящие от работы бота. Попробуйте запустить бота через 1-5 мин")
        ]


# Относительный путь к базе данных
DATABASE_PATH = 'database/database.db'

# Относительный путь к файлу с логами
LOGFILE_PATH = 'logs/debug.log'

# Параметр уровня логирования
LOG_LEVEL = 'DEBUG'

# Формат логирования
LOG_FORMAT = '{time:DD-MM-YYYY at HH:mm:ss} | {level: <8} | file: {file: ^30} | ' \
             'func: {function: ^30} | line: {line: >3} | message: {message}'

# Cписок администраторов -> загружается из файла .env
ADMINS = os.getenv('ADMINS')

# Время в секундах между сообщениями от пользователя, для контроля и защиты от 'флуда'
ANTIFLOOD_TIME = 1.5

# Время, временного ограничения доступа пользователя в секундах
# (устанавливается приложением автоматически, если пользователь флудит)
LIMITED_TIME = 120

# Максимальное количество попыток перезапуска бота в случае если он "упал" после ошибки
MAX_RESTART_BOT = 5
