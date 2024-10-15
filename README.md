# referral_system

Описание:
Необходимо разработать простой RESTful API сервис для реферальной системы.

Функциональные требования:
Регистрация и аутентификация пользователя (JWT, Oauth 2.0);
Аутентифицированный пользователь должен иметь возможность создать или удалить свой реферальный код. Одновременно может быть активен только 1 код. При создании кода обязательно должен быть задан его срок годности;
Возможность получения реферального кода по email 	адресу реферера;
Возможность регистрации по реферальному коду в 	качестве реферала;
Получение 	информации о рефералах по id 	реферера;
UI документация 	(Swagger/ReDoc).


## Технологии

- **FastAPI**: веб-фреймворк для создания API на Python.
- **SQLAlchemy**: библиотека для работы с базами данных.
- **PostgreSQL**: база данных.
- **Redis**: in-memory база данных для хранения реферальных кодов
- **Emailhunter**: сервис проверки почты


### Запуск проекта

Клонировать репозиторий и перейти в него в командной строке: 
```
https://github.com/LenarSag/referral_system
```
Cоздать и активировать виртуальное окружение: 
```
python3.9 -m venv venv 
```
* Если у вас Linux/macOS 

    ```
    source venv/bin/activate
    ```
* Если у вас windows 
 
    ```
    source venv/Scripts/activate
    ```
```
python3.9 -m pip install --upgrade pip
```
Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

Запуск проекта:
```
python main.py
```


Документация доступна после запуска по адресу:

http://127.0.0.1:8000/docs



### Примеры запросов

Прмер запроса POST на создание пользователя по реферальному коду: http://127.0.0.1:8000/api/v1/auth/user/12AF32CF8978

```json
{
    "username": "admin4", 
    "email": "test4@test.ru",
    "password": "Q123werty!23"
}
```

Ответ
```json
{
    "id": "5442a9ef-ea29-4d5c-a6ac-d29988e39cca",
    "email": "test4@test.ru",
    "username": "admin4"
}
```

Пример запроса POST на получение токена: http://127.0.0.1:8000/api/v1/auth/token

```json
{
    "username": "admin4", 
    "password": "Q123werty!23"
}
```

Ответ
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NDQyYTllZi1lYTI5LTRkNWMtYTZhYy1kMjk5ODhlMzljY2EiLCJleHAiOjE3MzE1ODQ4MjB9.HZNnpXvNbSHARx_aW3TJgVm8VxNmFTl-CHBdbOBzR9c",
    "token_type": "Bearer"
}
```

Пример запроса GET на получение списка рефералов: http://127.0.0.1:8000/api/v1/users/7c273bf082434c43b88d76ab0b6d1dff

Ответ
```json
{
    "items": [
        {
            "id": "5442a9ef-ea29-4d5c-a6ac-d29988e39cca",
            "email": "test4@test.ru",
            "username": "admin4"
        },
        {
            "id": "7ba606f3-8dd0-40b4-9aa0-ab5d7a632c58",
            "email": "test2@test.ru",
            "username": "admin3"
        },
        {
            "id": "e6ff06f8-7c30-4bb2-8682-4fc21530fc0b",
            "email": "test@test.ru",
            "username": "admin"
        }
    ],
    "total": 3,
    "page": 1,
    "size": 50,
    "pages": 1
}
```

Пример запроса POST на создание устаревшего реферального кода http://127.0.0.1:8000/api/v1/codes

```json
{
    "code": "FFFF12345678", 
    "expires_at": "2023-10-10 12:00"
}
```

Ответ
```json
{
    "detail": "Expires time less than current time"
}
```

Пример запроса POST на создание реферального кода http://127.0.0.1:8000/api/v1/codes

```json
{
    "code": "FFFF12345678", 
    "expires_at": "2025-10-10 12:00"
}
```

Ответ:
```json
{
    "id": 4,
    "user_id": "7c273bf0-8243-4c43-b88d-76ab0b6d1dff",
    "code": "FFFF12345678",
    "expires_at": "2025-10-10T12:00:00",
    "is_active": true
}
```


Пример запроса DELETE  на удаление реферального кода http://127.0.0.1:8000/api/v1/codes/JJJJ1234KKKK

Ответ

204 No content


Пример запроса GET на получение списка своих кодов http://127.0.0.1:8000/api/v1/codes/ 

Ответ
```json
{
    "items": [
        {
            "id": 1,
            "user_id": "7c273bf0-8243-4c43-b88d-76ab0b6d1dff",
            "code": "12AF32CF8978",
            "expires_at": "2021-09-11T12:00:00",
            "is_active": false
        },
        {
            "id": 2,
            "user_id": "7c273bf0-8243-4c43-b88d-76ab0b6d1dff",
            "code": "RT12OOOO1234",
            "expires_at": "2023-10-10T12:00:00",
            "is_active": false
        },
        {
            "id": 4,
            "user_id": "7c273bf0-8243-4c43-b88d-76ab0b6d1dff",
            "code": "FFFF12345678",
            "expires_at": "2025-10-10T12:00:00",
            "is_active": true
        }
    ],
    "total": 3,
    "page": 1,
    "size": 50,
    "pages": 1
}
```




Пример запроса GET на получение списка рефералов по id пользователя http://127.0.0.1:8000/api/v1/users/7c273bf082434c43b88d76ab0b6d1dff

Ответ
```json
{
    "items": [
        {
            "id": "5442a9ef-ea29-4d5c-a6ac-d29988e39cca",
            "email": "test4@test.ru",
            "username": "admin4"
        },
        {
            "id": "7ba606f3-8dd0-40b4-9aa0-ab5d7a632c58",
            "email": "test2@test.ru",
            "username": "admin3"
        },
        {
            "id": "e6ff06f8-7c30-4bb2-8682-4fc21530fc0b",
            "email": "test@test.ru",
            "username": "admin"
        }
    ],
    "total": 3,
    "page": 1,
    "size": 50,
    "pages": 1
}
```