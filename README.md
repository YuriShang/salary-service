1. Собрать контейнер
```
make build
```
2. Запустить контейнер
```
make run
```
3. Зарегистрировать нового пользователя
```
POST /signup
```

```json
{
    "first_name": "Ivan",
    "last_name": "Ivanov",
    "username": "user",
    "password": "pass"
}
```
4. Добавить информацию о зарплате и дате следующего повышения
```
POST /set_salary_info
```
```json
{
    "username": "user",
    "salary": 15000,
    "next_increase_date": "2024-06-29",
}
```
5. OAuth2 авторизация. Используем username и password. В случае успеха, сервис выдает токен, который действует 10 минут

```
Grant type - password
POST /login
```

6. Получить информацию о зарплате и дате следующего повышения. Необходима авторизация.
```
GET /get_salary
```
Пример ответа
```json
{
    "username": "user",
    "salary": 15000,
    "next_increase_date": "2024-06-29T00:00:00"
}
```
