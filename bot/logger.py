import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(funcName)s:%(lineno)d - %(message)s",
)

log_dir = Path(__file__).resolve().parent
log_dir.mkdir(parents=True, exist_ok=True)

file_handler = logging.FileHandler(log_dir / "Logs.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
