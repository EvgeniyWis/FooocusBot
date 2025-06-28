import logging
import os
from datetime import datetime, timedelta


class MoscowFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = datetime.fromtimestamp(record.created) + timedelta(hours=3)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            s = ct.strftime("%Y-%m-%d %H:%M:%S")
        return s

# Настройка логирования
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Используем наш кастомный форматтер
formatter = MoscowFormatter(
    "%(name)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)d - %(message)s",
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
