import datetime

from telebot.types import Message, CallbackQuery
from telebot_calendar import Calendar, RUSSIAN_LANGUAGE

from config_data.bot_messages import BotSays
from loader import bot, logger
from states.search_states import SearchState
from utils.decorators import exception_control
from utils.search_hotels import search_result

my_cnd = Calendar(language=RUSSIAN_LANGUAGE)


@exception_control.func_exception_control
def func_calendar(user_data: Message | CallbackQuery) -> None:
    """Создает и отправляет пользователю календарь 'travel_in' для выбора даты заезда"""
    bot.set_state(user_id=user_data.from_user.id, state=SearchState.travel_calendar)

    keyboard = Calendar.create_calendar(my_cnd, name='travel_in')
    bot.send_message(chat_id=user_data.from_user.id, text=BotSays.say('travel_in'), reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('travel'))
@exception_control.func_exception_control
def func_callback_calendar(call: CallbackQuery) -> None:
    """
    Отвечает пользователю в зависимости от выбранной даты календаря 'travel_in', если дата удовлетворяет условиям,
    записывает в базу данных дату заезда 'travel_in', создаёт и отправляет пользователю календарь 'travel_out'
    для выбора даты выезда. Затем отвечает пользователю в зависимости от выбранной даты календаря 'travel_out',
    если дата удовлетворяет условиям, записывает в базу данных количество дней, разницу между датой выезда и
    датой заезда. Условия выбора дат: дата заезда не может быть раньше текущей даты и дата выезда не может быть
    раньше даты заезда.
    """
    state: str | None = bot.get_state(user_id=call.from_user.id)

    if state and state.endswith('travel_calendar'):
        name, action, year, month, day = call.data.split(':')
        now_day = datetime.datetime.now().date()

        if action == 'DAY':
            incoming_day = datetime.date(int(year), int(month), int(day))

            if name == 'travel_in' and incoming_day >= now_day:
                bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                bot.send_message(chat_id=call.message.chat.id,
                                 text=f'Дата заселения:  <b>{incoming_day.strftime("%d.%m.%Y")}</b>')

                with bot.retrieve_data(user_id=call.from_user.id) as data:
                    data['date_in']: datetime = incoming_day

                keyboard = Calendar.create_calendar(my_cnd, name='travel_out')
                bot.send_message(chat_id=call.message.chat.id, text=BotSays.say('travel_out'), reply_markup=keyboard)

            elif name == 'travel_out':
                with bot.retrieve_data(user_id=call.from_user.id) as data:
                    in_date: datetime = data['date_in']

                if in_date and incoming_day > in_date:
                    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
                    bot.send_message(chat_id=call.message.chat.id,
                                     text=f'Дата отъезда:  <b>{incoming_day.strftime("%d.%m.%Y")}</b>')

                    with bot.retrieve_data(user_id=call.from_user.id) as data:
                        data['num_days']: int = (incoming_day - in_date).days

                    bot.set_state(user_id=call.from_user.id, state=SearchState.result)
                    search_result.func_result(call)
                else:
                    bot.answer_callback_query(call.id, text=BotSays.say('date order wrong'), show_alert=False)
            else:
                bot.answer_callback_query(call.id, text=BotSays.say('date not valid'), show_alert=False)

        elif action == "CANCEL":
            from handlers.command import reset
            bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
            reset.func_reset(user_data=call)

        else:
            Calendar.calendar_query_handler(my_cnd, bot=bot, call=call, name=name,
                                            action=action, year=year, month=month, day=day)

    else:
        bot.answer_callback_query(call.id, text=BotSays.old_keyboard(), show_alert=False)
        logger.debug(f'-> BAD -> keyboard does not match user state')
