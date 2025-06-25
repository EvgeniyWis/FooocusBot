import datetime
import logging
import os
import shutil
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path

log_dir = Path(__file__).resolve().parent / "logs"
backup_dir = log_dir / "backups"
log_dir.mkdir(parents=True, exist_ok=True)
backup_dir.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("tg_bot_logger")
logger.setLevel(logging.INFO)
logger.propagate = False

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)d - %(message)s",
)


def my_namer(default_name):
    dt = datetime.datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
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
