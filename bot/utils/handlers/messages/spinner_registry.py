LONG_PROMPT_PROCESSING_SPINNER_TEXT = "🧠 Обрабатываю длинный промпт..."

# Простой реестр для хранения одного спиннера на чат
_spinner_by_chat: dict[int, int] = {}

# Набор доступных констант-спиннеров (кортеж для неизменяемости)
SPINNER_TEXTS: tuple[str, ...] = (
    LONG_PROMPT_PROCESSING_SPINNER_TEXT,
)


def set_spinner(chat_id: int, message_id: int) -> None:
    _spinner_by_chat[chat_id] = message_id


def pop_spinner(chat_id: int) -> int | None:
    return _spinner_by_chat.pop(chat_id, None)


def get_spinner(chat_id: int) -> int | None:
    return _spinner_by_chat.get(chat_id) 