# dash_messenger
Мессенджер на технологии Websocket.
Этот проект является прямым продолжением [dash_websocket-chatrooms](https://github.com/MichaelODeli/dash_websocket-chatrooms). Только более масштабная реализация.

# Навигация
- **Описание приложения**
    - [Cтруктура проекта](#этапы-создания-приложения-roadmap)
    - [Планируемые возможности](#планируемые-возможности)
    - 🔄️ [Скриншоты приложения](/docs/SCREENSHOTS.md)
    - [Стек технологий](#стек-технологий)
    - [Установка и использование](#установка-и-использование)
- **Информация об обновлениях**
    - [Changelog](CHANGELOG.md)
    - [Система обозначения версий](/docs/VERSIONS.md)
- **Информация о компонентах приложения**
    - [Компоненты и функции frontend-а](/docs/COMPONENTS.md)
    - [Структура БД](/docs/DB_REFERENCE.md)
    - [Описание запросов и ответов WS-сервера](/docs/WS_SERVER_REFERENCE.md)
- **Отладка**
    - 🔄️ [Отладка сервера WebSocket](/server/ws_server/ws_server_tests.py)

## Стек технологий
- Технология обмена данными - **WebSocket**
- Frontend - [**Plotly Dash**](https://dash.plotly.com/) и дополнительные компоненты:
    - [dash-bootstrap-components](https://dash-bootstrap-components.opensource.faculty.ai/)
    - [dash-mantine-components (0.14.x)](https://www.dash-mantine-components.com/)
    - [dash-iconify](https://www.dash-mantine-components.com/dash-iconify)
    - [dash-extensions](https://www.dash-extensions.com/)
- Backend - [**Quart**](https://quart.palletsprojects.com/)

## Планируемые возможности
- Обмен сообщениями через Websocket в двустороннем канале
- Аккаунты для пользователей
    - Авторизация
        - ✅ Классическая
        - Двухфакторная
    - Регистрация
    - Восстановление аккаунта
    - Установка фото профиля
    - Настраиваемое имя пользователя
    - ✅ Ручной выход из аккаунта
- Общение с контактами
- Беседы с несколькими участниками
- ✅ Мобильная и ПК версии
- ✅ Светлая и темная версия сайта
- Отправка разных типов сообщений
    - Обычный текст
    - Форматированный текст (Markdown)
    - Фото
    - Стикеры (в т.ч. и пользовательские)
- ✅ Автоустановка проекта

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
        - ❌ Создание/редактирование бесед
        - Добавление контактов
        - Удаление чатов
        - Отправка стикеров
- 🔄️ **Создание WebSocket-сервера и базы данных**
    - ✅ Двусторонний обмен данными между сервером и клиентом 
    - ✅ Аутентификация соединений с помощью токенов
    - ✅ Проектирование структуры запросов и ответов
    - Разработка всех методов личной переписки и методов авторизации и регистрации
    - ✅ Проектирование и реализация БД на базе PostgreSQL
    - ✅ **Контейнеризация** проекта
        - ✅ Использование `docker-compose`
        - ✅ Автозапуск прод сервера и БД
        - ✅ Использование демо-данных для проверки работы мессенджера
        - ✅ Автоочистка недействующих токенов в процессе работы с другими пользователями (возможно нужен crontab)
        - ⚠️ Временно не разбирался с сетевой адресацией в docker. Могут быть проблемы.
    - ✅ Реализация работы обмена сообщениями на [специальной отладочной странице](/server/ws_server/ws_server_tests.py)
- **Соединение сервера и webUI**
    - Запросы сообщений и чатов через [background callbacks](https://dash.plotly.com/background-callbacks)
        - Запросы раз в 5 сек.
        - 🤔 Непонятно, кто должен инициировать обновление списка чатов и сообщений - сервер или клиент
        - ⚠️ При запросах чатов/сообщений отправляется сразу все данные, а не только новые
    - keep-alive и проверка соединения
    - Обработка ошибок в соединении
    - Подготовка итогового продукта в виде MVP
- **Модернизация**
    - Отправка разных видов контента (фото/видео/стикеры)
    - Работа многопользовательских бесед
    - Отображение прочтений сообщений
    - Улучшение методики обмена данными
        - При первоначальном запросе - отправляются сразу все данные
        - При повторных запросах - отправляются только новые данные

## Установка и использование
### Установка через docker-compose
1. `docker-compose build`
1. `docker-compose up`
### Ссылки на части проекта
- **webui** - [localhost:82](http://localhost:82)
- **База данных** - [localhost:6543](postgresql://postgres:postgres@localhost:6543/messenger) (port - `6543`, db - `messenger`, login:password - `postgres`/`postgres`)