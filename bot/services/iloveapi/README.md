# ILoveAPI Service

Сервис для работы с ILoveAPI - внешним сервисом для обработки изображений.

## Структура

```
services/iloveapi/
├── __init__.py              # Основные экспорты
├── client/
│   ├── __init__.py
│   └── api_client.py        # Основной клиент для работы с API
├── services/
│   ├── __init__.py
│   ├── upscaler.py          # Сервис для апскейла изображений
│   └── task_service.py      # Сервис для работы с задачами
├── utils/
│   ├── __init__.py
│   └── retry.py             # Утилиты для повторных попыток
└── types/
    └── __init__.py          # Типы данных
```

## Использование

### Базовое использование

```python
from bot.services.iloveapi import ILoveApiUpscaler

# Создание сервиса
upscaler = ILoveApiUpscaler()

# Апскейл изображения
result = await upscaler.upscale_image(
    temp_image_path="path/to/image.jpg",
    model_name="model_name",
    image_index=1,
    user_id=123,
    state=fsm_context
)
```

### Прямая работа с клиентом

```python
from bot.services.iloveapi import ILoveApiClient, ILoveApiTaskService

# Создание клиента
client = ILoveApiClient()

# Создание сервиса задач
task_service = ILoveApiTaskService(client)

# Обработка задачи
task = task_service.process_task_with_retry(
    file_path="path/to/file.jpg",
    task_type="upscaleimage",
    multiplier=4
)
```

## Особенности

- **Автоматические повторные попытки**: При ошибках 401 и других проблемах
- **Увеличенные таймауты**: Для работы с большими файлами
- **Альтернативные методы скачивания**: При проблемах с основным API
- **Логирование**: Подробное логирование всех операций
- **Обработка ошибок**: Детальная обработка различных типов ошибок

## Настройки

Сервис использует настройки из `bot.settings`:
- `PUBLIC_ILOVEAPI_API_KEY` - публичный ключ API
- `SECRET_ILOVEAPI_API_KEY` - секретный ключ API 