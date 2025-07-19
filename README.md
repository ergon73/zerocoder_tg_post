# zerocoder_tg_post

FastAPI приложение для автоматической генерации блог-постов на основе актуальных новостей с использованием OpenAI GPT-4 и 3. Укажите команду: `uvicorn app:app --host 0.0.0.0 --port $PORT`urrents API.

## 🚀 Возможности

- Генерация привлекательных заголовков статей
- Создание мета-описаний для SEO
- Написание структурированных постов с подзаголовками
- Интеграция с актуальными новостями через Currents API
- RESTful API для интеграции с другими сервисами

## 📋 Требования

- Python 3.8+
- OpenAI API ключ
- Currents API ключ

## 🛠️ Установка

1. **Клонируйте репозиторий:**
```bash
git clone https://github.com/your-username/zerocoder_tg_post.git
cd zerocoder_tg_post
```

2. **Создайте виртуальное окружение:**
```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

3. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

4. **Настройте API ключи:**

Скопируйте шаблон переменных окружения:
```bash
cp .env.example .env
```

Отредактируйте файл `.env` и добавьте ваши API ключи:
```bash
OPENAI_API_KEY=your_openai_api_key_here
CURRENTS_API_KEY=your_currents_api_key_here
```

## 🔑 Получение API ключей

- **OpenAI API**: https://platform.openai.com/api-keys
- **Currents API**: https://currentsapi.services/

## 🚀 Запуск

### Локальная разработка

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Продакшн

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## 📚 API Endpoints

### Основные эндпоинты

- `GET /` - Проверка работы сервиса
- `GET /heartbeat` - Проверка состояния
- `POST /generate-post` - Генерация поста

### Документация API

После запуска сервера откройте:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Пример запроса

```bash
curl -X POST "http://localhost:8000/generate-post" \
     -H "Content-Type: application/json" \
     -d '{"topic": "искусственный интеллект"}'
```

### Пример ответа

```json
{
  "title": "Искусственный интеллект: революция в технологиях",
  "meta_description": "Обзор последних достижений в области ИИ и их влияние на современный мир",
  "post_content": "Искусственный интеллект продолжает..."
}
```

## 🏗️ Структура проекта

```
zerocoder_tg_post/
├── app.py               # Основное приложение FastAPI
├── .env                 # Переменные окружения (не в git)
├── .env.example         # Шаблон для переменных окружения
├── requirements.txt     # Зависимости Python
├── Dockerfile          # Конфигурация Docker
├── docker-compose.yml  # Docker Compose конфигурация
├── .gitignore          # Исключения Git
└── README.md           # Документация
```

## 🌐 Деплой

### Koyeb

1. Создайте аккаунт на [Koyeb](https://koyeb.com)
2. Подключите GitHub репозиторий
3. В настройках приложения добавьте переменные окружения:
   - `OPENAI_API_KEY`
   - `CURRENTS_API_KEY`
4. Деплой автоматически запустится

### Render

1. Создайте аккаунт на [Render](https://render.com)
2. Подключите GitHub репозиторий
3. В Environment Variables добавьте:
   - `OPENAI_API_KEY`
   - `CURRENTS_API_KEY`
4. Укажите команду запуска: `uvicorn app:app --host 0.0.0.0 --port $PORT`

### Railway

1. Создайте аккаунт на [Railway](https://railway.app)
2. Подключите GitHub репозиторий
3. В Variables добавьте API ключи
4. Укажите команду: `uvicorn app2:app --host 0.0.0.0 --port $PORT`

## 🔧 Конфигурация

### Переменные окружения

| Переменная | Описание | Пример |
|------------|----------|--------|
| `OPENAI_API_KEY` | Ключ OpenAI API | `sk-...` |
| `CURRENTS_API_KEY` | Ключ Currents API | `...` |

### Локальная разработка

Используйте файл `.env` для локальной разработки:
```bash
OPENAI_API_KEY=your_key_here
CURRENTS_API_KEY=your_key_here
```

### Продакшн

Используйте переменные окружения платформы деплоя.

## 🐛 Отладка

### Логирование

Приложение использует расширенное логирование. В логах вы увидите:
- Загруженные API ключи
- Запросы к Currents API
- Ошибки генерации контента

### Проверка состояния

```bash
curl http://localhost:8000/heartbeat
```

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License

## 👨‍💻 Автор

ZeroCoder Team

---

**Примечание:** Не забудьте добавить `.env` в `.gitignore`, чтобы API ключи не попали в репозиторий! 

# Content Generation Service

## Переменные окружения

Для локальной разработки создайте файл `.env` в корне проекта со следующими переменными:

```env
# OpenAI API ключ для генерации контента
OPENAI_API_KEY=your_openai_api_key_here

# Currents API ключ для получения новостей
CURRENTS_API_KEY=your_currents_api_key_here

# Telegram бот токен (получить у @BotFather)
TELEGRAM_TOKEN=your_telegram_bot_token_here
```

⚠️ Файл `.env` добавлен в `.gitignore` и не будет отправлен в репозиторий.

## Настройка Telegram бота

1. Получите токен бота у [@BotFather](https://t.me/BotFather)
2. Добавьте токен в `.env` файл для локальной разработки
3. При деплое на сервер, добавьте переменную `TELEGRAM_TOKEN` в переменные окружения платформы
4. Настройте вебхук для бота, заменив `YOUR_TOKEN` и `YOUR_DOMAIN`:
```
https://api.telegram.org/botYOUR_TOKEN/setWebhook?url=https://YOUR_DOMAIN/telegram/webhook
```

### Команды бота

- `/start` - Получить приветственное сообщение и инструкции
- `/generate [тема]` - Сгенерировать контент по указанной теме 