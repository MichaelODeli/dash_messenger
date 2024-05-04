# dash_messenger
Мессенджер на технологии Websocket. Фронт и бэк на Dash (Flask), сервер на Quart.
Этот проект является прямым продолжением [dash_websocket-chatrooms](https://github.com/MichaelODeli/dash_websocket-chatrooms). Только более масштабная реализация)

## Ссылки на структурные части проекта
- ✅ [Cтруктура проекта](#этапы-создания-приложения)
- ✅ [Changelog](CHANGELOG.md)
- ✅ [Система обозначения версий](VERSIONS.md)
- [Скриншоты приложения](SCREENSHOTS.md)
- ✅ [Компоненты и функции](COMPONENTS.md)

## Планируемые возможности
- Обмен сообщениями через Websocket
    - В одном подключении идет получение сообщений с сервера (не только из активного диалога) и ответная их отправка
- Аккаунты для пользователей
    - ❌ Двухфакторная авторизация
    - Фото профиля
    - Ник и имя пользователя
- Общение с контактами
    - Добавление/удаление контактов
    - ❌ Создание бесед с несколькими участниками
- ✅ Мобильная и ПК версии
- ✅ Светлая и темная версия сайта
- Отправка разных типов сообщений
    - Обычный текст
    - ❌ Форматированный текст (Markdown)
    - ❌ Фото
    - ❌ Стикеры (в т.ч. и пользовательские)
- Автоустановка проекта

## Этапы создания приложения
*Список будет обновляться/дополняться по мере разработки.*
1. **Создание UI (т.н. webUI)**
    - > UI будет создан на разных страницах. Модалки могут быть вызваны с тех страниц, где они будут находиться.
    1. ✅ Страница авторизации
    1. ✅ Страница регистрации
    1. ✅ Страница восстановления пароля
    1. ✅ Страница личного кабинета
        1. ✅ Форма смены пароля
        1. ✅ Отображение почты и ника аккаунта
        1. ✅ Настройка приватности
        1. ❌ Справочный центр
    1. ✅ Страница мессенджера
        1. ✅ Левая сторона с контактами
        1. ✅ Правая сторона с сообщениями
    1. Модалки и всплывающие окна для мессенджера
        1. ✅ Прикрепление файлов
        1. ❌ Создание/редактирование бесед
        1. ✅ Добавление контактов
        1. ✅ Удаление чатов
        1. ✅ Отправка стикеров
1. **Проектирование и создание сервера (WebSocket)**
    1. Двусторонний обмен данными
    1. Проектирование структуры сообщения в JSON-формате
    1. Реализация непрерывного обмена сообщениями между контактами
1. **Создание real-time БД**
    1. Проектирование базы данных под пользовательские данные
    1. Реализация БД
    1. Нагрузочные тесты БД
1. **Соединение сервера и webUI**