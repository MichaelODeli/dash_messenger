# Структура запросов и ответов WS-сервера


# Содержание
- **[Основные поля](#основные-поля)**
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

# Основные поля
- `mode` - вид отправляемого запроса
- `timestamp` - время создания отправляемого запроса
- `status` - статус обработки запроса (в соответствии с [RFC 9110](https://httpwg.org/specs/rfc9110.html#overview.of.status.codes))
- `token` - токен для дальнейшего подписывания каждого отправляемого запроса

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
```python
{
    'mode': 'register',
    'timestamp': ...,
    'status': ...,
    'token': ...
}
```

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
`known_data_type`: `email`/`username`
### Ответ
> [!IMPORTANT]
> Метод восстановления аккаунта в разработке

## Выход (`logout`)
### Запрос
```python
{
    'mode': 'logout',
    'timestamp': ...,
    'token': ...,
    'username': ...
}
```
### Ответ
```python
{
    'mode': 'logout',
    'timestamp': ...,
    'status': ...,
}
```
# Сообщения
> Планируется, что поступающие сообщения будут передаваться на клиент без запросов.  
> Отправка сообщения с клиента - запись в БД - отправка сообщения из БД клиенту. 
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
```python
{
    'mode': 'getChats',
    'timestamp': ...,
    'status': ...,
    {
        {
            'chat_id': id,
            'chat_name': name, 
            'chat_type': personal/group
        }, ...
    }
}
```   

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
```python
{
    'mode': 'getMessages',
    'timestamp': ...,
    'status': ...,
    {
        {
            'from_id': ..., 
            'from_name': ..., 
            'content': ..., 
            'content_type': ...,
            'content_time': ...
        }, ...
    }
}
```   

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
```python
{
    'mode': 'sendMessage',
    'timestamp': ...,
    'status': ...,
}
```

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
```python
{
    'mode': 'sendGroupMessage',
    'timestamp': ...,
    'status': ...,
}
```