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
> >   "waste": <waste_id>,
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
> >   "current_capacity": 0
> > }
> > ```
>
> ### Изменить данные перерабатываемого отхода ###
> > ***Запрос***
> > - PUT по адресу ```127.0.0.1:8000/api/storage/<storage_id>/waste/<waste_id>/```
> > - Тело запроса:
> > ```
> > {
> >   "max_capacity": 10000
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
> >   "waste": <waste_id>,
> >   "value": 400
> > }
> > ```
>
> ### Обновить значение отхода ###
> > ***Запрос***
> > - PUT по адресу ```127.0.0.1:8000/api/org/<org_id>/generate/```
> > - Тело запроса:
> > ```
> > {
> >   "waste": <waste_id>,
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
