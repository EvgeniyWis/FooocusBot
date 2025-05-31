import logging
import os

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Создаем форматтер для логов
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Создаем директорию для логов если её нет
log_dir = os.path.dirname(os.path.abspath(__file__))
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Настройка вывода в файл
file_handler = logging.FileHandler(os.path.join(log_dir, "Logs.log"))
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Настройка вывода в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
