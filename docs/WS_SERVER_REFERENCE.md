# Структура запросов и ответов WS-сервера


# Содержание
- **[Основные поля](#основные-поля)**
- **[Проверки](#проверки)**
    - ✅ [Проверка соединения](#проверка-соединения-checkconnection)
    - ❌ [Проверка токена пользователя](#проверка-токена-checktoken)
- **[Аутентификация](#аутентификация)**
    - ✅ [Авторизация](#авторизация-auth)
    - ✅ [Регистрация](#регистрация-register)
    <!-- - [Восстановление аккаунта](#восстановление-аккаунта-recovery) -->
    - ✅ [Выход](#выход-logout)
- **Управление аккаунтом**
    - ❌ Смена никнейма
    - ❌ Смена почты
    - ❌ Установка фото профиля
- **[Сообщения](#сообщения)**
    - ✅ [Создание чата](#создание-чата-createpersonalchat)
    - ✅ [Получение списка чатов](#получение-списка-чатов-getchats)
    - ✅ [Получение сообщений в чате](#получение-сообщений-в-чате-getmessages)
    - ✅ [Отправка сообщения](#отправка-сообщения-sendmessage)
    - ❌ Удаление чата
- **Беседы**
    - ❌ Создание беседы
    - ❌ Отправка сообщения в беседу
    - ❌ Редактирование свойств беседы
    - ❌ Удаление беседы

# Основные поля
- `mode` - вид отправляемого запроса
- `timestamp` - время создания отправляемого запроса
- `status` - статус обработки запроса (в соответствии с [RFC 9110](https://httpwg.org/specs/rfc9110.html#overview.of.status.codes))
- `token` - токен для дальнейшего подписывания каждого отправляемого запроса

# Коды состояний
- **200** - ОК
- **401** - требуется авторизация для использования данного метода/невалидный токен
- **403** - превышение кол-ва доступных токенов
- **409** 
    - конфликт при регистрации (почта или имя пользователя уже есть в БД)
    - конфликт при создании чата/беседы (собеседник не найден)
- **422** - не все необходимые поля переданы
- **423** - отказ в попытке прочтения чатов, если человек не является его участником
- **500** - внутренняя ошибка сервера
- **501** - метод не реализован или не поддерживается


# Проверки

## Проверка соединения (`checkConnection`)
### Запрос
```python
{
    'mode': 'checkConnection',
    'timestamp': ...,
}
```
### Ответ
```python
{
    'mode': 'checkConnection',
    'timestamp': ...,
    'status': '200',
}
```

## Проверка токена (`checkToken`)
### Запрос
```python
{
    'mode': 'checkToken',
    'timestamp': ...,
    'token': ...
}
```
### Ответ
```python
{
    'mode': 'checkToken',
    'timestamp': ...,
    'status': ...,
}
```

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

<!-- ## Восстановление аккаунта (`recovery`)
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
> Метод восстановления аккаунта в разработке -->

## Выход (`logout`)
### Запрос
```python
{
    'mode': 'logout',
    'timestamp': ...,
    'token': ...
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
## Создание чата `createPersonalChat`
### Запрос
```python
{
    'mode': 'createChat',
    'timestamp': ...,
    'token': ...,
    'contact_value': ...,
    'contact_mode': ...
}
```
*contact_mode* - `id`/`username` (создание чата по нику или по id пользователя)
### Ответ
```python
{
    'mode': 'createChat',
    'timestamp': ...,
    'status': ...,
    'chat_id': ...
}
```

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
    'chats': [
        {
            'chat_id': id,
            'chat_members': ...,
            'chat_name': ..., 
            'chat_type': personal/group,
            'last_message_time': ...,
        ❌ 'last_message_text': ...
        ❌ 'last_message_sender': ... # for group
        }, ...
    ]
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
    'min_message_id': ...
}
```
- `min_message_id` - минимальный идентификатор сообщения (чтоб не получать одни и те же сообщения, можно передать этот параметр и передавать только новые сообщения, которые еще не отображены в диалоге). Параметр не обязательный.
### Ответ
```python
{
    'mode': 'getMessages',
    'timestamp': ...,
    'status': ...,
    'messages': [
        {
            'from_id': ..., 
            'from_name': ..., 
            'content': ..., 
            'content_type': ...,
            'content_time': ...
        }, ...
    ]
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