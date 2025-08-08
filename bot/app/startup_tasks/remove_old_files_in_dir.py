import os
import time

from bot.app.core.logging import logger


def remove_old_files_in_dir(directory_path: str, older_than_seconds: int) -> None:
    """Удаляет файлы и пустые папки в каталоге, старше указанного возраста.

    Не падает, если каталога нет.
    """
    try:
        if not os.path.exists(directory_path):
            return

        now = time.time()
        for root, _, files in os.walk(directory_path, topdown=False):
            for name in files:
                file_path = os.path.join(root, name)
                try:
                    if now - os.path.getmtime(file_path) > older_than_seconds:
                        os.remove(file_path)
                except Exception as e:
                    logger.warning(f"Не удалось удалить файл {file_path}: {e}")
    except Exception as e:
        logger.error(f"Ошибка при обходе каталога {directory_path}: {e}") 