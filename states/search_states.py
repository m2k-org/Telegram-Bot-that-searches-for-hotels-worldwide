from telebot.handler_backends import State, StatesGroup


class SearchState(StatesGroup):
    """Класс состояний пользователя"""

    command = State()
    location = State()
    show_num_hotels = State()
    yes_no_show_photos = State()
    show_num_photos_hotel = State()
    travel_calendar = State()
    range_price = State()
    range_distance = State()
    result = State()
    history = State()
    favorites = State()
    add_favorite = State()
