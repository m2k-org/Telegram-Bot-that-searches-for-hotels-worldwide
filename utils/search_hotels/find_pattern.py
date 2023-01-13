import json
import re

from telebot.types import Message, CallbackQuery

from loader import logger
from utils.decorators import exception_control


@exception_control.func_exception_control
def func_find_pattern(pattern: str, text: str, user_data: CallbackQuery | Message) -> dict | None:
    """Находит и возвращает шаблон(pattern) в тексте(text), если шаблон не найден, возвращает None."""

    result: re.Match = re.search(pattern, text)

    if result:
        found_to_pattern: dict = json.loads(f"{{{result[0]}}}")

        logger.debug(f'-> OK -> return -> found_to_pattern')
        return found_to_pattern

    logger.warning(f'-> BAD -> pattern: {pattern} -> not found in text: {text} -> return -> None')
    return None
