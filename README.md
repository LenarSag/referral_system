# referral_system

## в работе

http://127.0.0.1:8000/api/v1/auth/user/12AF32CF8978

```json
{
    "username": "admin4", 
    "email": "test4@test.ru",
    "password": "Q123werty!23"
}
```

```
{
    "id": "5442a9ef-ea29-4d5c-a6ac-d29988e39cca",
    "email": "test4@test.ru",
    "username": "admin4"
}
```


http://127.0.0.1:8000/api/v1/auth/token

{
    "username": "admin4", 
    "password": "Q123werty!23"
}


{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI1NDQyYTllZi1lYTI5LTRkNWMtYTZhYy1kMjk5ODhlMzljY2EiLCJleHAiOjE3MzE1ODQ4MjB9.HZNnpXvNbSHARx_aW3TJgVm8VxNmFTl-CHBdbOBzR9c",
    "token_type": "Bearer"
}


http://127.0.0.1:8000/api/v1/users/7c273bf082434c43b88d76ab0b6d1dff

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

http://127.0.0.1:8000/api/v1/codes

{
    "code": "FFFF12345678", 
    "expires_at": "2023-10-10 12:00"
}

{
    "detail": "Expires time less than current time"
}

http://127.0.0.1:8000/api/v1/codes

{
    "code": "FFFF12345678", 
    "expires_at": "2025-10-10 12:00"
}

{
    "id": 4,
    "user_id": "7c273bf0-8243-4c43-b88d-76ab0b6d1dff",
    "code": "FFFF12345678",
    "expires_at": "2025-10-10T12:00:00",
    "is_active": true
}


http://127.0.0.1:8000/api/v1/codes/JJJJ1234KKKK

204 No content



http://127.0.0.1:8000/api/v1/codes/ Получение списка своих кодов

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




http://127.0.0.1:8000/api/v1/users/7c273bf082434c43b88d76ab0b6d1dff


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