# dash_messenger
Мессенджер на технологии Websocket.
Этот проект является прямым продолжением [dash_websocket-chatrooms](https://github.com/MichaelODeli/dash_websocket-chatrooms). Только более масштабная реализация.

# Навигация
- **Описание приложения**
    - [Cтруктура проекта](#этапы-создания-приложения-roadmap)
    - [Скриншоты приложения](/docs/SCREENSHOTS.md)
    - [Стек технологий](#стек-технологий)
    - [Установка и использование](#установка-и-использование)
- **Информация об обновлениях**
    - [Changelog](CHANGELOG.md)
    - [Система обозначения версий](/docs/VERSIONS.md)
- **Информация о компонентах приложения**
    - [Компоненты и функции frontend-а](/docs/COMPONENTS.md)
    - [Структура БД](/docs/DB_REFERENCE.md)
    - [Описание запросов и ответов WS-сервера](/docs/WS_SERVER_REFERENCE.md)
    - [Описание запросов и ответов API-сервера](/docs/API_REFERENCE.md)
- **Отладка**
    - [Отладка сервера WebSocket](/server/ws_server/ws_server_tests.py)

## Стек технологий
- Технология обмена данными - **WebSocket**
- Frontend - [**Plotly Dash**](https://dash.plotly.com/) и дополнительные компоненты:
    - [dash-bootstrap-components](https://dash-bootstrap-components.opensource.faculty.ai/)
    - [dash-mantine-components (0.14.x)](https://www.dash-mantine-components.com/)
    - [dash-iconify](https://www.dash-mantine-components.com/dash-iconify)
    - [dash-extensions](https://www.dash-extensions.com/)
- Backend - [**Quart**](https://quart.palletsprojects.com/)

## Этапы создания приложения (roadmap)
*Список будет обновляться/дополняться по мере разработки.*
- ✅ **Создание UI (т.н. webUI)**
    - Страница авторизации
    - Страница регистрации
    - Страница восстановления пароля
    - Страница личного кабинета
        - Форма смены пароля
        - Отображение почты и ника аккаунта
        - Настройка приватности
        - ❌ Справочный центр
    - Страница мессенджера
        - Левая сторона с контактами
        - Правая сторона с сообщениями
    - Модалки и всплывающие окна для мессенджера
        - Прикрепление файлов
        - Добавление контактов
        - Удаление чатов
        - Отправка стикеров
- ✅ **Создание WebSocket-сервера и базы данных**
    - Двусторонний обмен данными между сервером и клиентом 
    - Аутентификация соединений с помощью токенов
        - ⚠️ Временно нет огранический по количеству токенов на один аккаунт
        - ⚠️ Отсутствует проверка IP пользователя при выдаче/проверке токена
    - Проектирование структуры запросов и ответов
    - Разработка всех методов личной переписки и основных методов работы с аккаунтом
        - ⚠️ Временно нет таймаутов для всех методов
        - ⚠️ Отсутствует дополнительная проверка регистрации через почту
        - ⚠️ Нет ограничений на кол-во персональных чатов с одним пользователем
    - Проектирование и реализация БД на базе PostgreSQL
    - **Контейнеризация** проекта
        - Использование `docker-compose`
        - Автозапуск прод сервера и БД
        - Использование демо-данных для проверки работы мессенджера
        - Автоочистка недействующих токенов в процессе работы с другими пользователями
    - Реализация работы обмена сообщениями на [специальной отладочной странице](/server/ws_server/ws_server_tests.py)
- 🔄️ **Соединение сервера и webUI**
    - Подготовка итогового продукта в виде MVP
    - Доработка основных страниц приложения
        - Главная (авторизация)
        - Регистрация
        - Мессенджер
    - Отключение тех страниц и кнопок, для которых не готова серверная часть
    - Поддержание непрерывного соединения между клиентом и сервером
    - Обработка ошибок
        - При потере соединения - блокировка полей ввода
        - При изначальной недоступности сервера - редирект на страницу с ошибкой
    - В случае нахождения двух клиентов в сети - общение проводится напрямую, в случае недоступности собеседника - сообщения помещаются в БД
- **Модернизация**
    - Дополнительные опции управления аккаунтом
        - Установка фото профиля
        - Смена почты
        - Смена пароля
        - Смена ника
        - Восстановление аккаунта
    - Отправка разных видов контента
        - Форматированный текст (Markdown)
        - Отправка фото
        - Отправка видео
        - Отправка стикеров
    - Работа многопользовательских бесед
        - Дополнительные модальные окна
        - Дополнительные методы для работы бесед
        - Доработка БД под многопользовательские беседы
    - Отображение прочтений сообщений
    - Справочный центр и работа поддержки (тикеты)
- **Переход на LTS**
    - Двухфакторная аутентификация
    - Финальное прописывание всех комментариев, документации и инструкций

## Установка и использование
### Установка через docker-compose
1. `docker-compose build`
1. `docker-compose up`
### Ссылки на части проекта
- **webui** - [localhost:82](http://localhost:82)
- **База данных** - localhost:6543 (port - `6543`, db - `messenger`, login:password - `postgres`/`postgres`)