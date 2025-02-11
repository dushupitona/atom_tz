# Тестовое задание 'Система учета отходов' #

> ## Запуск проекта ##
> 1. Склонируйте проект: ``` git clone https://github.com/dushupitona/atom_tz.git ```
> 2. Перейдите в директорию проекта: ``` cd atom_tz ```
> 3. Запустите команду ``` docker-compose up --build ```
>
> ## Сущности и модели ##
> ### Вид отхода ###
> - `name` - название отхода
>
> ### Хранилище ###
> - `name` - название хранилища
>
> ### Организация ###
> - `name` - название организации
>
> ### Хранилище и вид отхода ###
> *Модель связывающая хранилище с видом отхода*
> - `max_capacity` - объем хранилища для определенного отхода
> - `current_capacity` - текущий уровень заполненности хранилища определенным отходом
> - `remaining_capacity` - свободный объем хранилища
>
> ### Организация и хранилище ###
> *Модель связывающая организацию с хранилищем*
> - `interval` - расстояние между организацией и хранилищем
>
> ### Текущее значение отходов организации ###
> - `value` - значение определенного отхода организации
>
> ## Реализация ##
> В системе реализованы три основные сущности: `Вид отхода`, `Хранилище`, `Организация`. Связь между ними происходит через дополнительные модели, указанные выше. После создания и подключения всех сущностей организация может сгенерировать любой доступный вид отхода. Он будет положен на счет организации вместе с остальными отходами, откуда организация может отправить их на переработку. При достижении максимального запаса отхода в хранилище необработанный отход вернется на счет организации. Последовательность обхода хранилищей выбирается по наименьшему расстоянию.
>
> ## Тестовые данные ##
> - ***id: name***
>
> ***Виды отходов:***
> - 1: Bio
> - 2: Glass
> - 3: Plastic
>
> ***Хранилища:***
> - 1: Storage 1 \
>   *Обрабатываемые виды отходов:*
>   - Bio | *max_capacity:* 1000
>   - Glass | 500
>   - Plastic | 300
> - 2: Storage 2
>   - Bio | 460
>   - Glass | 700
> - 3: Storage 3
>   - Glass | 1300
> - 4: Storage 4
>   - Plastic | 2500
>
> ***Организации:***
> - 1: Organization 1 \
>   *Подключенные хранилища:*
>   - Storage 1 | *interval:* 5040
>   - Storage 2 | 2000
>   - Storage 3 | 3500
> - 2: Organization 2
>   - Storage 1 | 700
>   - Storage 2 | 4000
>   - Storage 4 | 1490
>
> ***Отходы организаций:***
> - 1: Organization 1 \
>   *Отходы:*
>   - Bio | *value:* 1100
>   - Glass | 1500
>   - Plastic | 800
> - 2: Organization 2
>   - Bio | 300
>   - Glass | 1150
>   - Plastic | 2700
>
> ## Админка Django ##
> Пользователь создается автоматически:
> - login: admin
> - password: admin
>
> ## Тестирование ##
> В проекте реализованы 60 unit-тестов, которые можно запустить при помощи команды ``` python manage.py test ```. \
> Также тестирование проходит автоматически при запуске проекта.
> 
> ---
> ## API ##
>
> ## *Вид отхода:* ##
> ### Создать объект отхода ###
> > ***Запрос***
> > - POST по адресу ```127.0.0.1:8000/api/waste/```
> > - Тело запроса:
> > ```
> > {
> >   "name": "waste_type_name"
> > }
> > ```
> 
> ### Получить список отходов ###
> > ***Запрос***
> > - GET по адресу ```127.0.0.1:8000/api/waste/```
> 
> > ***Ответ:***
> > ```
> > {
> >   [1, 2, 3]
> > }
> > ```
> 
> ### Получить данные отхода ###
> > ***Запрос***
> > - GET по адресу ```127.0.0.1:8000/api/waste/<waste_id>/```
> 
> > ***Ответ:***
> > ```
> > {
> >   "name": "waste_name"
> > }
> > ```
>
> ### Изменить данные отхода ###
> > ***Запрос***
> > - PUT по адресу ```127.0.0.1:8000/api/waste/<waste_id>/```
> > - Тело запроса:
> > ```
> > {
> >   "name": "new_waste_name"
> > }
> > ```
> 
> ### Удалить объект отхода ###
> > ***Запрос***
> > - DELETE по адресу ```127.0.0.1:8000/api/waste/<waste_id>/```
>
> ## *Хранилище:* ##
> ### Создать объект хранилища ###
> > ***Запрос***
> > - POST по адресу ```127.0.0.1:8000/api/storage/```
> > - Тело запроса:
> > ```
> > {
> >   "name": "storage_name"
> > }
> > ```
> 
> ### Получить список хранилищей ###
> > ***Запрос***
> > - GET по адресу ```127.0.0.1:8000/api/storage/```
> 
> > ***Ответ:***
> > ```
> > {
> >   [1, 2, 3]
> > }
> > ```
> 
> ### Получить данные хранилища ###
> > ***Запрос***
> > - GET по адресу ```127.0.0.1:8000/api/storage/<storage_id>/```
> 
> > ***Ответ:***
> > ```
> > {
> >   "name": "storage_name"
> > }
> > ```
>
> ### Изменить данные хранилища ###
> > ***Запрос***
> > - PUT по адресу ```127.0.0.1:8000/api/storage/<storage_id>/```
> > - Тело запроса:
> > ```
> > {
> >   "name": "new_storage_name"
> > }
> > ```
> 
> ### Удалить объект хранилища ###
> > ***Запрос***
> > - DELETE по адресу ```127.0.0.1:8000/api/storage/<storage_id>/```
>
> ## *Хранилище & вид отхода* ##
> ### Добавить в хранилище перерабатываемый вид отхода ###
> > ***Запрос***
> > - POST по адресу ```127.0.0.1:8000/api/storage/<storage_id>/waste/```
> > - Тело запроса:
> > ```
> > {
> >   "waste_type": <waste_id>,
> >   "max_capacity": 7000
> > }
> > ```
>
> ### Получить список перерабатываемых отходов ###
> > ***Запрос***
> > - GET по адресу ```127.0.0.1:8000/api/storage/<storage_id>/waste/```
> 
> > ***Ответ:***
> > ```
> > {
> >   [1, 2, 3]
> > }
> > ```
>
> ### Получить данные перерабатываемого отхода ###
> > ***Запрос***
> > - GET по адресу ```127.0.0.1:8000/api/storage/<storage_id>/waste/<waste_id>/```
> 
> > ***Ответ:***
> > ```
> > {
> >   "max_capacity": 7000,
> >   "current_capacity": 500,
> >   "remaining_capacity": 6500
> > }
> > ```
>
> ### Изменить данные перерабатываемого отхода ###
> > ***Запрос***
> > - PUT по адресу ```127.0.0.1:8000/api/storage/<storage_id>/waste/<waste_id>/```
> > - Тело запроса:
> > ```
> > {
> >   "max_capacity": 10000,
> >   "current_capacity": 0
> > }
> > ```
> 
> ### Удалить перерабатываемый отход ###
> > ***Запрос***
> > - DELETE по адресу ```127.0.0.1:8000/api/storage/<storage_id>/waste/<waste_id>/```
>
> ## *Организация:* ##
> ### Создать объект организации ###
> > ***Запрос***
> > - POST по адресу ```127.0.0.1:8000/api/org/```
> > - Тело запроса:
> > ```
> > {
> >   "name": "org_name"
> > }
> > ```
> 
> ### Получить список организаций ###
> > ***Запрос***
> > - GET по адресу ```127.0.0.1:8000/api/org/```
> 
> > ***Ответ:***
> > ```
> > {
> >   [1, 2, 3]
> > }
> > ```
> 
> ### Получить данные организации ###
> > ***Запрос***
> > - GET по адресу ```127.0.0.1:8000/api/org/<org_id>/```
> 
> > ***Ответ:***
> > ```
> > {
> >   "name": "org_name",
> >   "waste": {
> >       <waste_id>: <value>,
> >       ...
> >   }
> > }
> > ```
>
> ### Изменить данные организации ###
> > ***Запрос***
> > - PUT по адресу ```127.0.0.1:8000/api/org/<org_id>/```
> > - Тело запроса:
> > ```
> > {
> >   "name": "new_org_name"
> > }
> > ```
> 
> ### Удалить объект организации ###
> > ***Запрос***
> > - DELETE по адресу ```127.0.0.1:8000/api/org/<org_id>/```
>
> ## *Организация & хранилище* ##
> ### Подключить хранилище к организации ###
> > ***Запрос***
> > - POST по адресу ```127.0.0.1:8000/api/org/<org_id>/storage/```
> > - Тело запроса:
> > ```
> > {
> >   "storage": <storage_id>,
> >   "interval": 1250
> > }
> > ```
>
> ### Получить список подключенных хранилищ ###
> > ***Запрос***
> > - GET по адресу ```127.0.0.1:8000/api/org/<org_id>/storage/```
> 
> > ***Ответ:***
> > ```
> > {
> >   [1, 2, 3]
> > }
> > ```
>
> ### Получить данные подключенного хранилища ###
> > ***Запрос***
> > - GET по адресу ```127.0.0.1:8000/api/org/<org_id>/storage/<storage_id>/```
> 
> > ***Ответ:***
> > ```
> > {
> >   "interval": 1250
> > }
> > ```
>
> ### Изменить данные подключенного хранилища ###
> > ***Запрос***
> > - PUT по адресу ```127.0.0.1:8000/api/org/<org_id>/storage/<storage_id>/```
> > - Тело запроса:
> > ```
> > {
> >   "interval": 2000
> > }
> > ```
> 
> ### Отключить хранилище ###
> > ***Запрос***
> > - DELETE по адресу ```127.0.0.1:8000/api/org/<org_id>/storage/<storage_id>/```
> 
> ## *Переработка отходов* ##
> ### Сгенерировать отход ###
> > ***Запрос***
> > - POST по адресу ```127.0.0.1:8000/api/org/<org_id>/generate/```
> > - Тело запроса:
> > ```
> > {
> >   "waste_type": <waste_id>,
> >   "value": 400
> > }
> > ```
>
> ### Изменить значение отхода ###
> > ***Запрос***
> > - PUT по адресу ```127.0.0.1:8000/api/org/<org_id>/generate/```
> > - Тело запроса:
> > ```
> > {
> >   "waste_type": <waste_id>,
> >   "value": 0
> > }
> > ```
>
> ### Отправить отходы на переработку ###
> > ***Запрос***
> > - POST по адресу ```127.0.0.1:8000/api/org/<org_id>/send/```
> 
> > ***Ответ***
> > ```
> > {
> >   "storage_responses": {
> >     "1": "completely",
> >     "2": "partially",
> >     "3": "crowded",
> >     "4": "no_storage"
> >   },
> >   "total_distance": 1750
> > }
> > ```
> > ***Статусы обработки отхода***
> > - `completely` - отход обработан полностью
> > - `partially` - отход обработан частично (закончилось место в хранилищах)
> > - `crowded` - отход не обработан (все хранилища с этим типом отхода заполнены)
> > - `no_storage` - отход не обработан (отсутствует хранилище для этого типа отхода)
