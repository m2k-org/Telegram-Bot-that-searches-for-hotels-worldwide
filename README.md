# ___Funny bot  for Search Hotels___ 

<font size = 2><i> Developed by [Kouyate Moussa](https://github.com/m2kouyate), September 2022.</i></font>

___
Телеграм бот для поиска отелей по всему миру.
___
<a id="ceiling"></a>

### __Установка приложения:__

1. Для установки бота на свой компьютер или сервер клонируйте этот репозиторий командой: 
   <i><span style="color:  #228B22;"> git clone ссылка на репозиторий </span><i>

2. Установите зависимости из файла [requirements.txt](requirements.txt) командой: 
   <i><span style="color:  #228B22;"> pip install -r requirements.txt </span></i>

3. Создайте бота при помощи [BotFather](https://telegram.me/BotFather), полученный токен необходимо указать 
   в переменной [<span style="color:  #228B22;">BOT_TOKEN</span>](.env.template) файла [.env.template](.env.template) 
   вместо текста в кавычках (кавычки оставить).

4. Зарегистрируйтесь на сайте [RapidAPI](https://rapidapi.com/apidojo/api/hotels4/), 
   выберите подходящий тариф, полученный токен необходимо указать в переменной 
   [<span style="color:  #228B22;">RAPID_API_KEY</span>](.env.template) файла [.env.template](.env.template) вместо 
   текста в кавычках (кавычки оставить).

5. Переменная [<span style="color:  #228B22;">ADMINS</span>](.env.template) в файле [.env.template](.env.template) - это список 
   id пользователей Telegram, которым будут предоставлены права администраторов вашего бота. Чтобы узнать id, необходимо 
   зайти в поисковую строку приложения Telegram и ввести <i><span style="color:  #228B22;">@getmyid_bot</span></i>, 
   активировать первого бота в списке, в ответ он пришлет уникальный id пользователя. Можно не указывать, либо указать 
   позднее, удалив текст и оставив пустые кавычки. 

6. Обязательно необходимо переименовать файл [.env.template](.env.template) в <i><span style="color:  #228B22;">.env
   </span></i> На этом установка завершена, запускайте файл [main.py](main.py) и пользуйтесь вашим приложением.

### __Настройка бота:__

- [config.py](config_data/config.py) - пользовательские настройки, с описанием. 

- [bot_messages](config_data/bot_messages.py) - словарь сообщений для удобства редактирования текста сообщений от бота пользователю 

### __Структура репозитория и документация:__
<ul><details><summary><b><i><span style="color:  #6495ED;">показать</span></i></b></summary>

[.env.template](.env.template)
   
    файл с конфиденциальной информацией (перед запуском бота, внести изменения и переименовать в .env).

[loader.py](loader.py)

    файл настраивающий и подгружающий необходимые модули для запуска бота.

[main.py](main.py)

    запуск бота, в случае 'падения' происходит перезапуск бота количество раз(MAX_RESTART_BOT), 
    при: старте, рестарте и отключении бота отправляется сообщение администраторам.

[requirements.txt](requirements.txt)

    файл с информацией о зависимостях проекта, названием и релизом, необходимых для работы бота библиотек.

[<span style="color:  #228B22;">config_data</span>](config_data)

    Папка с конфигурационными файлами 
&emsp; &emsp; &emsp; [bot_messages.py](config_data/bot_messages.py)

            BotSays
               Класс методов, возвращающих значения словаря SAYS сообщений от бота пользователю
            say
               Метод извлекает из стека вызовов имя файла, в котором он был вызван и использует это имя в качестве первого
               ключа, если указан key, он используется в качестве второго ключа для извлечения значения словаря
               сообщений от бота пользователю.

&emsp; &emsp; &emsp; [config.py](config_data/config.py)

            Пользовательские настройки приложения

[<span style="color:  #228B22;">database</span>](database)

    Папка с базой данных и её утилитами

&emsp; &emsp; &emsp; [database.db](database/database.db)

            База данных пользователей приложения, содержит id пользователя, имя пользователя, права доступа 
            пользователя, историю запросов от пользователя. А также информацию о курсе USD по данным ЦБ РФ.
&emsp; &emsp; &emsp; [database_utility.py](database/database_utility.py)

            В этом файле описаны функции для работы приложения с базой данных

[<span style="color:  #228B22;">handlers</span>](handlers)

    Папка с обработчиками сообщений от пользователя

&emsp; [<span style="color:  #228B22;">callback_from_keyboards</span>](handlers/callback_from_keyboards)
     
      Папка с обработчиками обратного вызова клавиатур

&emsp; &emsp; &emsp; [get_calendar.py](handlers/callback_from_keyboards/get_calendar.py)

            func_calendar
                  Создает и отправляет пользователю календарь 'travel_in' для выбора даты заезда

            func_callback_calendar
                  Отвечает пользователю в зависимости от выбранной даты календаря 'travel_in', если дата удовлетворяет условиям,
                  записывает в базу данных дату заезда 'travel_in', создаёт и отправляет пользователю календарь 'travel_out'
                  для выбора даты выезда. Затем отвечает пользователю в зависимости от выбранной даты календаря 'travel_out',
                  если дата удовлетворяет условиям, записывает в базу данных количество дней, разницу между датой выезда и
                  датой заезда. Условия выбора дат: дата заезда не может быть раньше текущей даты и дата выезда не может быть
                  раньше даты заезда.
&emsp; &emsp; &emsp; [get_history.py](handlers/callback_from_keyboards/get_history.py)

            func_get_history
                  Обработчик обратного вызова с Inline клавиатуры ключу("key_hist"), отправляет сообщение пользователю в
                  зависимости от нажатой кнопки(callback) и сбрасывает состояние пользователя.
&emsp; &emsp; &emsp; [delete_history.py](handlers/callback_from_keyboards/delete_history.py)

            func_del_history
                  Обработчик обратного вызова с Inline клавиатуры ключу("del_hist"), отправляет сообщение пользователю в
                  зависимости от нажатой кнопки(callback) и сбрасывает состояние пользователя.
&emsp; &emsp; &emsp; [get_favorite.py](handlers/callback_from_keyboards/get_favorite.py)

            func_get_favorite
                  Обработчик обратного вызова с Inline клавиатуры ключу("key_favor"), отправляет сообщение пользователю в
                  зависимости от нажатой кнопки(callback) и сбрасывает состояние пользователя.
&emsp; &emsp; &emsp; [delete_favorite.py](handlers/callback_from_keyboards/delete_favorite.py)

            func_del_favorites
                  Обработчик обратного вызова с Inline клавиатуры ключу("del_favor"), отправляет сообщение пользователю в
                  зависимости от нажатой кнопки(callback) и сбрасывает состояние пользователя.
&emsp; &emsp; &emsp; [get_add_favorites.py](handlers/callback_from_keyboards/get_add_favorites.py)

            func_get_yes_no_favorite
                  Обработчик обратного вызова с Inline клавиатуры ключу("fav"), отправляет сообщение пользователю в
                  зависимости от нажатой кнопки(callback) и сбрасывает состояние пользователя.
&emsp; &emsp; &emsp; [get_location.py](handlers/callback_from_keyboards/get_location.py)

            func_get_location
                  Обработчик обратного вызова с Inline клавиатуры ключу("key_csk"), отправляет сообщение пользователю в
                  зависимости от нажатой кнопки(callback), сохраняет данные в базу данных, изменяет состояние пользователя
                  или сбрасывает запрос.
            func_to_show_num_hotels
                  Отправляет пользователю клавиатуру для выбора количества отелей к показу и изменяет состояние пользователя.
&emsp; &emsp; &emsp; [get_show_num_hotels.py](handlers/callback_from_keyboards/get_show_num_hotels.py)

            func_get_num_hotels
                  Обработчик обратного вызова с Inline клавиатуры по ключу("key_snh"), отправляет сообщение пользователю в
                  зависимости от нажатой кнопки(callback), сохраняет данные в базу данных и изменяет состояние пользователя.
&emsp; &emsp; &emsp; [get_show_num_photos_hotel.py](handlers/callback_from_keyboards/get_show_num_photos_hotel.py)

            func_get_num_photos
                  Обработчик обратного вызова с Inline клавиатуры по ключу("key_sph"), отправляет сообщение пользователю в
                  зависимости от нажатой кнопки(callback), изменяет состояние пользователя.
&emsp; &emsp; &emsp; [get_yes_no_show_photos.py](handlers/callback_from_keyboards/get_yes_no_show_photos.py)

            func_get_yes_no_photos
                  Обработчик обратного вызова с Inline клавиатуры ключу("key_yn"), отправляет сообщение пользователю в
                  зависимости от нажатой кнопки(callback), сохраняет данные в базу данных и изменяет состояние пользователя.
                        
&emsp; [<span style="color:  #228B22;">command</span>](handlers/command)
    
      Папка с обработчиками команд
&emsp; &emsp; &emsp; [favorites.py](handlers/command/favorites.py)

            func_favorites
                  Обработчик команды /favorites, отправляет клавиатуру с датами избранных отелей пользователя или сообщение об
    отсутствии избранных.
&emsp; &emsp; &emsp; [help.py](handlers/command/help.py)

            func_help
                  Обработчик команды /help, отправляет разъясняющее сообщение пользователю в зависимости от его состояния.
&emsp; &emsp; &emsp; [history.py](handlers/command/history.py)

            func_history
                  Обработчик команды /history, отправляет клавиатуру с датами истории поиска пользователя или сообщение об отсутствии
                  истории поиска. 
&emsp; &emsp; &emsp; [reset.py](handlers/command/reset.py)

            func_reset
                  Обработчик команды /reset, сбрасывает состояние пользователя, также используется как функция сброса состояния
                  в случае исключения в процессе обработки запроса от пользователя. 
&emsp; &emsp; &emsp; [search_commands.py](handlers/command/search_commands.py)

            func_search_commands
                  Обработчик команд(lowprice, highprice, bestdeal), запускает сценарий поиска и сортировки отелей.
&emsp; &emsp; &emsp; [start.py](handlers/command/start.py)

            start
                  Обработчик команды /start от пользователя, если пользователь не найден в базе данных, записывает его, таким образом
                  запускает процесс взаимодействия бота с пользователем или отправляет пользователю сообщение -> бот уже запущен.
&emsp; [<span style="color:  #228B22;">other</span>](handlers/other) 

      Папка с обработчиками различных данных поступающих от пользователя
&emsp; &emsp; &emsp; [any_contents_but_text.py](handlers/other/any_contents_but_text.py)

            func_any_message
                  Обработчик не текстовых данных полученных от пользователя, для реакции бота на сообщения. 
&emsp; &emsp; &emsp; [any_text.py](handlers/other/any_text.py)

            func_any_text
                  Обработчик не распознанных текстовых данных, введенных с клавиатуры устройства пользователя, в любом состоянии
                  пользователя, для реакции бота на сообщения. 
&emsp; &emsp; &emsp; [get_city.py](handlers/other/get_city.py)

            func_get_city
                  Обработчик данных, введенных с клавиатуры устройства пользователя, в состоянии пользователя SearchState.command,
                  логика ожидает ввода пользователем названия города для поиска отелей в нём.
            
&emsp; &emsp; &emsp; [get_ranges.py](handlers/other/get_ranges.py)

            func_get_ranges
                  Обработчик данных, введенных с клавиатуры устройства пользователя, в состояниях пользователя
                  SearchState.range_price или SearchState.range_distance, логика ожидает ввода пользователем диапазонов цен и
                  расстояний в виде двух чисел через пробел для установки критериев поиска отелей.

[<span style="color:  #228B22;">keyboards</span>](keyboards) 
   
    Папка с инлайн клавиатурами
&emsp; &emsp; &emsp; [add_favorite_keyboard.py](keyboards/add_favorite_keyboard.py)

            func_add_favorites_keyboard
                  Создаёт и возвращает клавиатуру да/ нет, в callback дата запроса и ключ для handler.
&emsp; &emsp; &emsp; [choice_number_keyboard.py](keyboards/choice_number_keyboard.py)

            func_number_keyboard
                  Создаёт и возвращает нумерованную клавиатуру, в callback название номер(button), ключ(key) для handler.
&emsp; &emsp; &emsp; [city_selection_keyboard.py](keyboards/city_selection_keyboard.py)

            city_keyboard
                  Создаёт и возвращает клавиатуру по количеству городов в списке(cities), в callback название города, его id и
                  ключ для фильтра callback_query_handler, в названии города установленно ограничение по длине текста, чтобы не
                  превышать максимально допустимый размер callback в inline кнопке в 64 байта. 
&emsp; &emsp; &emsp; [date_favorite_keyboard.py](keyboards/date_favorite_keyboard.py)

            func_favorite_keyboard
                  Создаёт и возвращает нумерованную клавиатуру по количеству строк в сохраненной избранных пользователя,
    в callback дата запроса и ключ для handler.
&emsp; &emsp; &emsp; [date_history_keyboard.py](keyboards/date_history_keyboard.py)

            func_history_keyboard
                  Создаёт и возвращает нумерованную клавиатуру по количеству строк в сохраненной истории запросов пользователя,
                  в callback дата запроса и ключ для handler.

&emsp; &emsp; &emsp; [yes_no_keyboard.py](keyboards/yes_no_keyboard.py)

            func_keyboard
                  Создает и возвращает клавиатуру с двумя кнопками Да и Нет, в callback да/нет и ключ для handler.

[<span style="color:  #228B22;">logs</span>](logs) 

    Папка с log файлами записывающими ход исполнения скрипта проекта и регистрацией ошибок.

[<span style="color:  #228B22;">middlewares</span>](middlewares)

    Папка с промежуточными, предварительными обработчиками сообщений от пользователя
&emsp; &emsp; &emsp; [access_control.py](middlewares/access_control.py)

            AccessControlMiddleware
                  Проверяет права доступа пользователя к приложению записанные в базе данных, если доступ разрешен или
                  пользователь не найден в базе, пропускает сообщение пользователя к дальнейшей обработке, также передаёт далее
                  данные о пользователе полученные из базы данных, предварительно записав их в словарь data.
&emsp; &emsp; &emsp; [flood_control.py](middlewares/flood_control.py)

            FloodControlMiddleware
                  Контролирует время между сообщениями от пользователя для защиты от "флуда". 
&emsp; &emsp; &emsp; [state_and_user_control.py](middlewares/state_and_user_control.py)

            StateControlMiddleware
                  Контролирует соответствие сообщений от пользователя его состоянию, в случае не соответствия
                  отправляет пользователю сообщение и сбрасывает дальнейшую обработку сообщения.

[<span style="color:  #228B22;">states</span>](states)

    Папка с модулем сосотояний 
&emsp; &emsp; &emsp; [search_states.py](states/search_states.py)

            SearchState
                  Класс состояний пользователя

[<span style="color:  #228B22;">utils</span>](utils)

    Папка с утилитами проекта
&emsp; [<span style="color:  #228B22;">decorators</span>](utils/decorators) 

      Папка с декораторами функций 
&emsp; &emsp; &emsp; [exception_control.py](utils/decorators/exception_control.py)

            func_exception_control
                  Декоратор, контролирует выполнение кода в функции, в случае успешного выполнения возвращает результат
                  выполнения функции, в случае исключения вызывает функцию reset.func_reset для сброса состояния пользователя
                  и возвращает None.

&emsp; [<span style="color:  #228B22;">misc</span>](utils/misc)

      Папка с прочими утилитами
&emsp; &emsp; &emsp; [admins_send_message.py](utils/misc/admins_send_message.py)

            func_admins_message
                  Отправляет сообщения об ошибках и состоянии бота администраторам, если их id указаны в ADMINS.
&emsp; &emsp; &emsp; [usd_rate.py](utils/misc/usd_rate.py)

            func_rate
                  Возвращает курс USD и дату сохраненные в базе данных, если данные устарели более чем на RATE_UPDATE,
                  обновляет их, запрашивая актуальные данные на сайте URL_cbr, и возвращает обновленные курс USD и дату.

&emsp; [<span style="color:  #228B22;">search_hotels</span>](utils/search_hotels) 

      Папка с утилитами поиска отелей
&emsp; &emsp; &emsp; [add_favorites.py](utils/search_hotels/add_favorites.py)

            func_add_favorites
                  Предлагает пользователю добавить историю поиска в избранное и записывает результат поиска отелей в базу
    данных.
&emsp; &emsp; &emsp; [find_city_locations.py](utils/search_hotels/find_city_locations.py)

            func_find_location
                  Находит и возвращает список локаций(found_cities) по названию города(incoming_city) введенного пользователем,
                  если запрос к API(response_from_api) успешный, а локации по шаблону(pattern) в нём не найдены возвращает None.
&emsp; &emsp; &emsp; [find_hotel_photos.py](utils/search_hotels/find_hotel_photos.py)

            func_find_photos
                  Находит и возвращает список фотографий(photos) отеля(hotels), в случае исключения(KeyError) возвращает пустой список.
&emsp; &emsp; &emsp; [find_hotels_in_city.py](utils/search_hotels/find_hotels_in_city.py)

            func_find_hotels
                  Находит и возвращает отели(hotels) в городе(city_id) или None.
&emsp; &emsp; &emsp; [find_hotels_in_ranges.py](utils/search_hotels/find_hotels_in_ranges.py)

            find_in_ranges
                  Проверяет каждый отель из списка отелей на соответствие диапазонам цен и расстояний, в случае несоответствия
                  отель удаляется из списка, если после проверки список окажется пустым, выводится сообщение
                  пользователю и запрос сбрасывается.
&emsp; &emsp; &emsp; [find_pattern.py](utils/search_hotels/find_pattern.py)

            func_find_pattern
                  Находит и возвращает шаблон(pattern) в тексте(text), если шаблон не найден, возвращает None.
&emsp; &emsp; &emsp; [hotel_info.py](utils/search_hotels/hotel_info.py)

            func_hotel_info
                  Формирует и возвращает сообщение для пользователя с информацией об отеле(hotel) по доступным данным
&emsp; &emsp; &emsp; [ranges.py](utils/search_hotels/ranges.py)

            func_range
               Устанавливает состояние соответствующее определенной установке диапазонов, отправляет сообщение пользователю.

&emsp; &emsp; &emsp; [request_api.py](utils/search_hotels/request_api.py)

            func_request
                  Запрашивает данные с API сайта(url) по заголовкам(HEADERS) и ключам(querystring), если они указаны, в случае успеха
                  возвращает полученное сообщение в виде строки, в противном случае возвращает None и отправляет сообщение об ошибке
                  запроса администраторам.
&emsp; &emsp; &emsp; [search_result.py](utils/search_hotels/search_result.py)

            func_result
                  Отправляет пользователю результат поиска отелей согласно сценарию(command) от пользователя и
                  записывает его в базу данных истории поиска.
&emsp; &emsp; &emsp; [sort_hotels.py](utils/search_hotels/sort_hotels.py)

            func_sort_hotels
                  Сортирует отели по выбранному сценарию:
                  /highprice: сначала дорогие
                  /lowprice: сначала дешёвые
                  /bestdeal: двойная сортировка дешевые отели ближе всего к центру
            sort_price
                  Возвращает стоимость отеля, если её нет в словаре возвращает 99,99
            sort_city_center
                  Возвращает расстояние до центра, если его нет в словаре возвращает 99,99
&emsp; [set_bot_commands.py](utils/set_bot_commands.py)

            set_default_commands
                  Устанавливает команды в меню бота

</details></ul>

### __Команды бота:__

<ul><summary><b><i><span style="color:  #6495ED;">/start</span></i></b> - запуск бота</summary>
</ul>

<ul><summary><b><i><span style="color:  #6495ED;">/help</span></i></b> - справка о возможных действиях</summary>
</ul>

<ul><summary><b><i><span style="color:  #6495ED;">/lowprice</span></i></b> - топ дешёвых отелей в городе</summary>
</ul>

<ul><summary><b><i><span style="color:  #6495ED;">/highprice</span></i></b> - топ дорогих отелей в городе</summary>
</ul>

<ul><summary><b><i><span style="color:  #6495ED;">/bestdeal</span></i></b> - топ дешёвых отелей ближе к центру</summary>
</ul>

<ul><summary><b><i><span style="color:  #6495ED;">/history</span></i></b> - история поиска отелей</summary>
</ul>

<ul><summary><b><i><span style="color:  #6495ED;">/favorites</span></i></b> - избранное</summary>
</ul>

<ul><summary><b><i><span style="color:  #6495ED;">/reset</span></i></b> - сброс текущего запроса</summary>
</ul>

### __Дополнительные функции администрирования:__
В случае "падения" бота, в результате ошибки в программе предусмотрен перезапуск, их максимальное количество указано 
в переменной [<span style="color:  #228B22;">MAX_RESTART_BOT</span>](config_data/config.py), файла 
[config.py](config_data/config.py)

Для оперативного контроля ошибок, в случае исключения администраторам отправляется сообщение об ошибке с указанием 
файла, в котором она произошла, строки, кода и пользователя, у которого произошло исключение.    



[наверх](#ceiling)

