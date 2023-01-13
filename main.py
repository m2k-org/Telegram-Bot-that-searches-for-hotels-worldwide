import time
from art import tprint
from telebot.custom_filters import StateFilter

import middlewares
from loader import bot, logger
from utils.set_bot_commands import set_default_commands
from utils.misc.admins_send_message import func_admins_message

if __name__ == '__main__':

    def start(restart=0):
        """
        Запуск бота, в случае 'падения' происходит перезапуск бота количество раз(MAX_RESTART_BOT), при: старте,
        рестарте и отключении бота отправляется сообщение администраторам.
        """
        try:
            tprint('Bot by Moussa K.')
            logger.info('-> START_BOT <-')
            func_admins_message(message=f'<b>БОТ ЗАПУЩЕН</b> &#128640')

            set_default_commands(bot)
            bot.add_custom_filter(StateFilter(bot))
            bot.setup_middleware(middlewares.access_control.AccessControlMiddleware())
            bot.setup_middleware(middlewares.flood_control.FloodControlMiddleware())
            bot.setup_middleware(middlewares.state_and_user_control.StateControlMiddleware())
            bot.infinity_polling()

        except BaseException as exc:
            logger.exception(exc)

            from config_data.config import MAX_RESTART_BOT
            func_admins_message(message=f'&#9762&#9760 <b>BOT CRITICAL ERROR</b> &#9760&#9762\n'
                                        '<b>File</b>: main.py\n'
                                        f'<b>Exception</b>: {exc.__class__.__name__}\n'
                                        f'<b>Traceback</b>: {exc}')

            if MAX_RESTART_BOT - restart:
                restart += 1
                func_admins_message(message=f'&#9888<b>WARNING</b>&#9888\n<b>10 seconds to {restart} restart BOT</b>!')
                logger.info(f'-> 10 seconds to {restart} restart BOT <-')
                time.sleep(10)

                start(restart=restart)

            else:
                func_admins_message(message=f'&#9760<b>BOT IS DEAD</b>&#9760')
                logger.info('-> BOT IS DEAD <-')

    start()
