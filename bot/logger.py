import logging
import os
import shutil
from datetime import datetime, timedelta
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path


class MoscowFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = datetime.fromtimestamp(record.created) + timedelta(hours=3)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            s = ct.strftime("%Y-%m-%d %H:%M:%S")
        return s


log_dir = Path(__file__).resolve().parent / "logs"
backup_dir = log_dir / "backups"
log_dir.mkdir(parents=True, exist_ok=True)
backup_dir.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("tg_bot_logger")
logger.setLevel(logging.INFO)
logger.propagate = False

# Используем наш кастомный форматтер
formatter = MoscowFormatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)d - %(message)s",
)


def my_namer(default_name):
    dt = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return str(backup_dir / dt / "logs.log")


def my_rotator(source, dest):
    os.makedirs(Path(dest).parent, exist_ok=True)
    shutil.copy2(source, dest)
    open(source, "w").close()


if not logger.handlers:
    file_handler = TimedRotatingFileHandler(
        filename=log_dir / "Logs.log",
        when="midnight",
        interval=1,
        backupCount=7,
        encoding="utf-8",
        utc=True,
    )
    file_handler.setFormatter(formatter)
    file_handler.namer = my_namer
    file_handler.rotator = my_rotator
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
