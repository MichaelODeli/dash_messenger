# Компоненты и функции приложения
Вспомогательный файл для ведения учета идентификаторов блоков и функций.

---

# Компоненты и идентификаторы блоков
## Header
- **Кнопки**
    - `color-mode-switch` - переключение темы приложения
    - `navbar-toggler` - скрыть/развернуть элементы навбара при переполнении

## Окно авторизации
> [!IMPORTANT]
> Раздел наполняется

## Окно восстановления аккаунта
> [!IMPORTANT]
> Раздел наполняется

## Окно регистрации
> [!IMPORTANT]
> Раздел наполняется

## Окно управления аккаунтом
> [!IMPORTANT]
> Раздел наполняется

## Окно мессенджера
### Колонка контактов
- **Кнопки**
    - `messenger-btn-contacts_actions` - действия над контактами
        - `messenger-btn-create_chat` - создание беседы
        - `messenger-btn-add_contact` - добавление контакта
    - `messenger-btn-open_contacts_drawer` - открыть боковую панель с контактами (доступно с мобильных устройств)
- **Таблицы**
    - `messenger-table-contacts` - таблица контактов
- **Drawer**
    - `messenger-drawer-contacts` - drawer с контактами (доступно с мобильных устройств)
### Колонка мессенджера
- **Кнопки**
    - `messenger-btn-attachment_actions` - действия над вложениями
        - `messenger-btn-attachment_photo` - отправка фото
        - `messenger-btn-attachment_video` - отправка видео
        - `messenger-btn-attachment_file` - отправка файла
    - `messenger-btn-send`
    - `downClick` - прокрутка таблицы с сообщениями вниз
    - `messenger-btn-chat_actions` - действия над собеседником
        - `messenger-btn-toggle_notif` - переключить уведомления
        - `messenger-btn-delete_chat` - удалить чат
        - `messenger-btn-ban` - заблокировать собеседника
- **Таблицы**
    - `messenger-table-stickers` - таблица стикеров (`4 столбца*7рядов*50px`)
    - `messenger-table-messages` - таблица с сообщениями
- **Поля ввода текста**
    - `messenger-input-message_text` - текст сообщения
- **Изображения**
    - `messenger-img-chat_partner` - аватарка собеседника
- **Вывод текста**
    - `messenger-text-chat_partner_nickname` - ник собеседника

# Функции - генераторы элементов