import logging
import os
import shutil
from contextvars import ContextVar
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


# Контекстные переменные для пользователя
current_user_id: ContextVar[str] = ContextVar("current_user_id", default="-")
current_username: ContextVar[str] = ContextVar("current_username", default="-")


class UserContextFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.user_id = current_user_id.get()
        record.username = current_username.get()
        return True


# Корень пакета bot
package_root = Path(__file__).resolve().parents[1]
log_dir = package_root / "logs"
backup_dir = log_dir / "backups"
log_dir.mkdir(parents=True, exist_ok=True)
backup_dir.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("tg_bot_logger")
logger.setLevel(logging.INFO)
logger.propagate = False
# Добавляем фильтр пользовательского контекста
logger.addFilter(UserContextFilter())

# Используем наш кастомный форматтер
formatter = MoscowFormatter(
    "%(asctime)s - %(name)s - %(levelname)s - [user_id=%(user_id)s username=%(username)s] - %(filename)s:%(funcName)s:%(lineno)d - %(message)s",
)


def my_namer(default_name):
    dt = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    return str(backup_dir / dt / "logs.log")


def my_rotator(source, dest):
    os.makedirs(Path(dest).parent, exist_ok=True)
    shutil.copy2(source, dest)
    open(source, "w").close()
    cleanup_old_backups()


def cleanup_old_backups(max_backups=7):
    backups = sorted(backup_dir.iterdir(), key=os.path.getmtime)
    if len(backups) > max_backups:
        for old in backups[:-max_backups]:
            logger.info(f"Removing old backup: {old}")
            shutil.rmtree(old)


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