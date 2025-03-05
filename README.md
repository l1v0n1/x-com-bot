# X.com AI Bot

# English version

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered bot for automatically responding to mentions on X.com (Twitter) using local language models through Ollama.

[Русская версия документации](#русская-версия)

## Features

- Monitor mentions and replies using Twitter API v2
- Analyze context and generate relevant responses using Ollama models
- Automatic response posting with API rate limit handling
- Comprehensive logging and error handling

## Requirements

- Python 3.8+
- [Ollama](https://ollama.ai/) for running local models
- Minimum 8 GB RAM
- About 3-8 GB free space per model
- Twitter API v2 access (Essential tier or higher)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/l1v0n1/x-com-bot.git
cd x-com-bot
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install and run Ollama:
```bash
# Installation instructions: https://ollama.ai/download
# After installation, run:
ollama serve
```

4. Install models:
```bash
# List available models
ollama list

# Pull a model (examples):
ollama pull deepseek-r1:1.5b  # ~4.37 GB
ollama pull llama3:8b         # ~3.8 GB
ollama pull mistral:7b        # ~4.1 GB
ollama pull neural:7b         # ~4.1 GB

# View model details
ollama info MODEL_NAME
```

5. Create a `.env` file with your API keys:
```env
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token
MODEL_NAME=deepseek-r1:1.5b  # Name of installed model to use
```

## Model Management

### Available Models
You can find a list of available models at [Ollama Library](https://ollama.ai/library).
Some recommended models for this bot:

1. `deepseek-r1:1.5b` (default)
   - Size: ~4.37 GB
   - Good balance of quality and speed
   - Recommended for most users

2. `llama3:8b`
   - Size: ~3.8 GB
   - Faster responses
   - Lower RAM usage

3. `mistral:7b`
   - Size: ~4.1 GB
   - High quality responses
   - Good multilingual support

### Model Commands
```bash
# List installed models
ollama list

# Remove a model
ollama rm MODEL_NAME

# Update a model
ollama pull MODEL_NAME

# Get model information
ollama info MODEL_NAME
```

### Switching Models
1. Stop the bot if running
2. Install new model using `ollama pull MODEL_NAME`
3. Update MODEL_NAME in your `.env` file
4. Restart the bot

## Usage

Run the bot:
```bash
python run_bot.py
```

The bot will:
1. Check for available models
2. Use the model specified in .env (or default)
2. Monitor mentions and replies
4. Generate and post responses
5. Log all actions to `bot.log`

## Project Structure

```
x_com_bot/
├── __init__.py
├── bot.py           # Main bot class
├── config.py        # Configuration loader
├── model_manager.py # Ollama model management
└── run_bot.py       # Entry point
```

## Security

- API keys stored in `.env` file (not included in repository)
- Automatic rate limit handling
- Retry mechanisms for API errors
- Model integrity verification

## Logging

- All actions logged to `bot.log`
- Log rotation at 500 MB
- Detailed error information

## Performance

- Response generation time: ~2-3 seconds
- RAM usage: ~4-6 GB
- Automatic request delay management

## Error Handling

- Automatic retries for API errors
- Graceful degradation for model issues
- Detailed debugging logs

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Twitter API Setup

### Required Permissions
Your Twitter API app must have the following permissions enabled:
- Read and Write
- Read and Write Direct Messages
- Manage Tweets

To set these permissions:
1. Go to [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Select your project and app
3. Go to "User authentication settings"
4. Enable OAuth 1.0a
5. Select the required permissions
6. Save changes and regenerate tokens

### Rate Limits
The bot includes automatic rate limit handling:
- Waits when Twitter API limits are reached
- Logs waiting time and resumes automatically
- Distributes requests evenly to avoid limits

If you encounter rate limits frequently, consider:
- Increasing the check interval in `.env`:
  ```env
  CHECK_INTERVAL=120  # Check every 120 seconds instead of default 60
  ```
- Using Twitter API v2 Essential access or higher
- Monitoring `bot.log` for rate limit patterns

---

# Русская версия

[English version](#english-version)

Бот для автоматического ответа на упоминания в X.com (Twitter) с использованием локальной языковой модели через Ollama.

## Функциональность

- Мониторинг упоминаний и ответов через Twitter API v2
- Анализ контекста и генерация релевантных ответов с помощью моделей из Ollama
- Автоматическая публикация ответов с соблюдением лимитов API
- Логирование всех действий и обработка ошибок

## Требования

- Python 3.8+
- [Ollama](https://ollama.ai/) для запуска локальной модели
- Минимум 8 GB RAM
- 3-8 GB свободного места для каждой модели
- Доступ к Twitter API v2 (Essential или выше)

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/l1v0n1/x-com-bot.git
cd x-com-bot
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Установите и запустите Ollama:
```bash
# Инструкции по установке: https://ollama.ai/download
# После установки запустите:
ollama serve
```

4. Установите модели:
```bash
# Посмотреть доступные модели
ollama list

# Установить модель (примеры):
ollama pull deepseek-r1:1.5b  # ~4.37 GB
ollama pull llama3:8b         # ~3.8 GB
ollama pull mistral:7b        # ~4.1 GB
ollama pull neural:7b         # ~4.1 GB

# Посмотреть информацию о модели
ollama info ИМЯ_МОДЕЛИ
```

5. Создайте файл `.env` с вашими API ключами:
```env
TWITTER_API_KEY=your_api_key
TWITTER_API_SECRET=your_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
TWITTER_BEARER_TOKEN=your_bearer_token
MODEL_NAME=deepseek-r1:1.5b  # Имя установленной модели для использования
```

## Управление моделями

### Доступные модели
Список всех доступных моделей можно найти в [библиотеке Ollama](https://ollama.ai/library).
Рекомендуемые модели для бота:

1. `deepseek-r1:1.5b` (по умолчанию)
   - Размер: ~4.37 GB
   - Хороший баланс качества и скорости
   - Рекомендуется для большинства пользователей

2. `llama3:8b`
   - Размер: ~3.8 GB
   - Быстрые ответы
   - Меньше потребление RAM

3. `mistral:7b`
   - Размер: ~4.1 GB
   - Высокое качество ответов
   - Хорошая поддержка разных языков

### Команды для работы с моделями
```bash
# Список установленных моделей
ollama list

# Удалить модель
ollama rm ИМЯ_МОДЕЛИ

# Обновить модель
ollama pull ИМЯ_МОДЕЛИ

# Информация о модели
ollama info ИМЯ_МОДЕЛИ
```

### Смена модели
1. Остановите бота если он запущен
2. Установите новую модель через `ollama pull ИМЯ_МОДЕЛИ`
3. Обновите MODEL_NAME в файле `.env`
4. Перезапустите бота

## Использование

Запустите бота:
```bash
python run_bot.py
```

Бот будет:
1. Проверять доступные модели
2. Использовать модель указанную в .env (или по умолчанию)
3. Отслеживать упоминания и ответы
4. Генерировать и публиковать ответы
5. Записывать все действия в `bot.log`

## Структура проекта

```
x_com_bot/
├── __init__.py
├── bot.py           # Основной класс бота
├── config.py        # Загрузка конфигурации
├── model_manager.py # Управление Ollama моделью
└── run_bot.py       # Точка входа
```

## Безопасность

- API ключи хранятся в `.env` файле (не включен в репозиторий)
- Автоматическая обработка rate limits
- Повторные попытки при ошибках API
- Проверка целостности модели

## Логирование

- Все действия записываются в `bot.log`
- Ротация лога при достижении 500 MB
- Подробная информация об ошибках

## Производительность

- Время генерации ответа: ~2-3 секунды
- Использование RAM: ~4-6 GB
- Автоматическое управление задержками между запросами

## Обработка ошибок

- Автоматические повторные попытки при ошибках API
- Graceful degradation при проблемах с моделью
- Подробное логирование для отладки

## Настройка Twitter API

### Необходимые разрешения
Ваше приложение Twitter API должно иметь следующие разрешения:
- Read and Write (Чтение и запись)
- Read and Write Direct Messages (Чтение и отправка личных сообщений)
- Manage Tweets (Управление твитами)

Для настройки разрешений:
1. Перейдите в [Twitter Developer Portal](https://developer.twitter.com/en/portal/dashboard)
2. Выберите ваш проект и приложение
3. Перейдите в "User authentication settings"
4. Включите OAuth 1.0a
5. Выберите необходимые разрешения
6. Сохраните изменения и перегенерируйте токены

### Ограничения API
Бот автоматически обрабатывает ограничения API:
- Ожидает при достижении лимитов Twitter API
- Логирует время ожидания и автоматически возобновляет работу
- Распределяет запросы равномерно для избежания лимитов

Если часто возникают ограничения:
- Увеличьте интервал проверки в `.env`:
  ```env
  CHECK_INTERVAL=120  # Проверка каждые 120 секунд вместо 60 по умолчанию
  ```
- Используйте Twitter API v2 Essential или выше
- Отслеживайте `bot.log` для анализа паттернов ограничений