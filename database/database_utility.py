import sqlite3

from config_data import config
from loader import logger
from utils.decorators import exception_control
from collections import namedtuple

# В этом файле описаны функции для работы приложения с базой данных


def create_table():
    with sqlite3.connect(config.DATABASE_PATH) as database:
        cursor = database.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS users( 
                          user_id INTEGER PRIMARY KEY,
                          user_name TEXT,
                          access TEXT,
                          start_time_limited INTEGER)"""
                       )
        cursor.execute("""CREATE TABLE IF NOT EXISTS search_history( 
                          user_id INTEGER,
                          data TEXT,
                          searches TEXT)"""
                       )
        cursor.execute("""CREATE TABLE IF NOT EXISTS favorites( 
                                  user_id INTEGER,
                                  date_info TEXT)"""
                       )
        cursor.execute("""CREATE TABLE IF NOT EXISTS rates( 
                                  rate_USD INTEGER,
                                  date_rate TEXT,
                                  time_record INTEGER)"""
                       )
        database.commit()
        logger.debug('-> OK -> CREATE TABLES IF NOT EXISTS in database')


@exception_control.func_exception_control
def select_rate(user_data):
    rate = namedtuple('rate', ['rate_USD', 'date_rate', 'time_record'])
    with sqlite3.connect(config.DATABASE_PATH) as database:
        cursor = database.cursor()
        cursor.execute("SELECT rate_USD, date_rate, time_record FROM rates")
        data = cursor.fetchone()
    if data:
        rate = rate(*data)
    else:
        rate = None
    logger.debug(f'-> OK -> SELECT -> return -> {rate}')
    return rate


@exception_control.func_exception_control
def update_rate(rate, date, time, user_data):
    with sqlite3.connect(config.DATABASE_PATH) as database:
        cursor = database.cursor()
        cursor.execute("UPDATE rates SET rate_USD = ?, date_rate = ?, time_record = ?", (rate, date, time))
        database.commit()
    logger.debug(f'-> OK -> UPDATE rate: {rate}, date: {date} time: {time} in database')


@exception_control.func_exception_control
def insert_rate(rate, date, time, user_data):
    with sqlite3.connect(config.DATABASE_PATH) as database:
        cursor = database.cursor()
        cursor.execute("INSERT INTO rates(rate_USD, date_rate, time_record) VALUES (?, ?, ?)", (rate, date, time))
        database.commit()
    logger.debug(f'-> OK -> INSERT rate: {rate}, date: {date}, time: {time} in database')


@exception_control.func_exception_control
def select_user(user_id, user_data):
    user = namedtuple('user', ['user_id', 'user_name', 'access', 'start_time_limited'])
    with sqlite3.connect(config.DATABASE_PATH) as database:
        cursor = database.cursor()
        cursor.execute("SELECT user_id, user_name, access, start_time_limited FROM users WHERE user_id = ?", (user_id,))
        data = cursor.fetchone()
    if data:
        user = user(*data)
    else:
        user = None
    logger.debug(f'-> OK -> SELECT -> return -> {user}')
    return user


@exception_control.func_exception_control
def update_user_access(user_data, user_id, access, start_time_limited=None):
    with sqlite3.connect(config.DATABASE_PATH) as database:
        cursor = database.cursor()
        cursor.execute("UPDATE users SET access = ?, start_time_limited = ? WHERE user_id = ?",
                       (access, start_time_limited, user_id))
        database.commit()


@exception_control.func_exception_control
def insert_user(user_data, user_id, name, access, start_time_limited=None):
    with sqlite3.connect(config.DATABASE_PATH) as database:
        cursor = database.cursor()
        cursor.execute("INSERT INTO users(user_id, user_name, access, start_time_limited) VALUES (?, ?, ?, ?)",
                       (user_id, name, access, start_time_limited))
        database.commit()


@exception_control.func_exception_control
def select_history_dates(user_id, user_data):
    with sqlite3.connect(config.DATABASE_PATH) as database:
        cursor = database.cursor()
        cursor.execute("SELECT data FROM search_history WHERE user_id = ?", (user_id,))
        history_dates = cursor.fetchall()

    if len(history_dates) > 25:
        num_dates = len(history_dates) - 25
        del history_dates[:num_dates]
    return history_dates


@exception_control.func_exception_control
def select_favorites_dates(user_id, user_data):
    with sqlite3.connect(config.DATABASE_PATH) as database:
        cursor = database.cursor()
        cursor.execute("SELECT date_info FROM favorites_results WHERE user_id = ?", (user_id,))
        favorites_dates = cursor.fetchall()
    return favorites_dates


@exception_control.func_exception_control
def select_searches(user_id, date, user_data):
    with sqlite3.connect(config.DATABASE_PATH) as database:
        cursor = database.cursor()
        cursor.execute("SELECT searches FROM search_history WHERE user_id = ? AND data = ?", (user_id, date))
        history = cursor.fetchone()
    return history


@exception_control.func_exception_control
def select_favorites(user_id, date, user_data):
    with sqlite3.connect(config.DATABASE_PATH) as database:
        cursor = database.cursor()
        cursor.execute("SELECT searches FROM favorites_results WHERE user_id = ? AND data = ?", (user_id, date))
        favorite = cursor.fetchone()
    return favorite


@exception_control.func_exception_control
def insert_history(user_id, date, history, user_data):
    with sqlite3.connect(config.DATABASE_PATH) as database:
        cursor = database.cursor()
        cursor.execute("INSERT INTO search_history(user_id, data, searches) VALUES (?, ?, ?)", (user_id, date, history))
        database.commit()


@exception_control.func_exception_control
def insert_favorite(user_id, date_info, user_data):
    with sqlite3.connect(config.DATABASE_PATH) as database:
        cursor = database.cursor()
        cursor.execute("INSERT INTO favorites(user_id, date_info) VALUES (?, ?)", (user_id, date_info))
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites_results AS
            SELECT favorites.user_id, date_info, search_history.searches
            FROM search_history
            JOIN favorites
            ON favorites.date_info = search_history.data AND favorites.user_id = search_history.user_id
        """)

        database.commit()


@exception_control.func_exception_control
def remove_history(user_id, user_data):
    with sqlite3.connect(config.DATABASE_PATH) as database:
        cursor = database.cursor()
        cursor.execute("DELETE from search_history WHERE user_id = ?", (user_id,))
        database.commit()


@exception_control.func_exception_control
def remove_favorite(user_id, user_data):
    with sqlite3.connect(config.DATABASE_PATH) as database:
        cursor = database.cursor()
        cursor.execute("DELETE from favorites_results WHERE user_id = ?", (user_id,))
        database.commit()
