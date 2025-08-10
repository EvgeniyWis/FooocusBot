import asyncio

import bot.app.config.constants as constants
from bot.app.core.logging import logger
from bot.app.config.settings import settings

from .remove_old_files_in_dir import remove_old_files_in_dir


async def periodic_cleanup_task() -> None:
    """Периодическая очистка временных файлов старше TTL.

    Охватывает каталоги: bot/temp/images, bot/temp/videos, temp, .assets/images/temp
    """
    ttl_seconds = settings.TEMP_FILES_TTL_HOURS * 3600
    interval_seconds = settings.TEMP_CLEANUP_INTERVAL_MINUTES * 60
    target_dirs = [
        str(constants.TEMP_IMAGE_FILES_DIR),
        str(constants.TEMP_VIDEOS_FILES_DIR),
        str(constants.FACEFUSION_TEMP_IMAGES_FOLDER_PATH),
        str(constants.FACEFUSION_RESULTS_DIR),
        str(constants.TEMP_FILES_DIR),
    ]

    logger.info(
        f"Запущена фоновая очистка временных файлов: ttl={settings.TEMP_FILES_TTL_HOURS}ч, interval={settings.TEMP_CLEANUP_INTERVAL_MINUTES}м"
    )
    while True:
        try:
            for d in target_dirs:
                remove_old_files_in_dir(d, ttl_seconds)
        except Exception as e:
            logger.error(f"Ошибка при периодической очистке временных файлов: {e}")
        await asyncio.sleep(interval_seconds) 