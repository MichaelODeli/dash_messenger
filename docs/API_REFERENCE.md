# API Reference

## Верификация токена (GET)
### Содержание заголовков
- `Authorization` - токен аккаунта
- `Sec-Fetch-Mode` - `token_validation`
### Варианты ответов
- **Успех** - True, 200
- **Токен не валидный** - False, 200