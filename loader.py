from loguru import logger
from telebot import TeleBot
from telebot.storage import StateMemoryStorage

from config_data import config
from database import database_utility

storage = StateMemoryStorage()

bot: TeleBot = TeleBot(token=config.BOT_TOKEN, parse_mode='HTML', state_storage=storage, use_class_middlewares=True)

database_utility.create_table()

logger.add(sink=config.LOGFILE_PATH, format=config.LOG_FORMAT, level=config.LOG_LEVEL, diagnose=True, backtrace=False,
           rotation="500 kb", retention=3, compression="zip")
