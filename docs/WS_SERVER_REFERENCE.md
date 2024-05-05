# Структура запросов и ответов WS-сервера


# Содержание
- **[Аутентификация](#аутентификация)**
    - [Авторизация](#авторизация-auth)
    - [Регистрация](#регистрация-register)
    - [Восстановление аккаунта](#восстановление-аккаунта-recovery)
    - [Выход](#выход-logout)
- **[Сообщения](#сообщения)**
    - [Получение списка чатов](#получение-списка-чатов-getchats)
    - [Получение сообщений в чате](#получение-сообщений-в-чате-getmessages)
    - [Отправка сообщения](#отправка-сообщения-sendmessage)
    - [Отправка сообщения в беседу](#отправка-сообщения-в-беседу-sendgroupmessage)


# Аутентификация

## Авторизация (`auth`)
### Запрос
```python
{
    'mode': 'auth',
    'timestamp': ...,
    'username': ...,
    'password': ...
}
```
### Ответ
```python
{
    'mode': 'auth',
    'timestamp': ...,
    'status': ...,
    'token': ...
}
```

## Регистрация (`register`)
### Запрос
```python
{
    'mode': 'register',
    'timestamp': ...,
    'username': ...,
    'password': ...,
    'email': ...
}
```
### Ответ
> [!IMPORTANT]
> Раздел наполняется

## Восстановление аккаунта (`recovery`)
### Запрос
```python
{
    'mode': 'recovery',
    'timestamp': ...,
    'username': ...,
    'known_data': ...,
    'known_data_type': ...
}
```
- `known_data_type`: `email`/`username`
### Ответ
> [!IMPORTANT]
> Раздел наполняется

## Выход (`logout`)
### Запрос
```python
{
    'mode': 'logout',
    'timestamp': ...,
    'token': ...,
}
```
### Ответ
> [!IMPORTANT]
> Раздел наполняется

# Сообщения
> Планируется, что поступающие сообщения будут передаваться на клиент без запросов.  
> Отправка сообщения с клиента - запись в БД - отправка сообщения из БД клиенту.   
> Методы `get` служат для первичного получения списка сообщений. Отправляемые 
## Получение списка чатов `getChats`
### Запрос
```python
{
    'mode': 'getChats',
    'timestamp': ...,
    'token': ...,
}
```
### Ответ
> [!IMPORTANT]
> Раздел наполняется

## Получение сообщений в чате `getMessages`
### Запрос
```python
{
    'mode': 'getMessages',
    'timestamp': ...,
    'token': ...,
    'chat_id': ...
}
```
### Ответ
> [!IMPORTANT]
> Раздел наполняется

## Отправка сообщения `sendMessage`
### Запрос
```python
{
    'mode': 'sendMessage',
    'timestamp': ...,
    'token': ...,
    'chat_id': ...,
    'content': ...,
    'content_type': ...
}
```
### Ответ
> [!IMPORTANT]
> Раздел наполняется

## Отправка сообщения в беседу `sendGroupMessage`
### Запрос
```python
{
    'mode': 'sendGroupMessage',
    'timestamp': ...,
    'token': ...,
    'chat_id': ...,
    'content': ...,
    'content_type': ...
}
```
### Ответ
> [!IMPORTANT]
> Раздел наполняется