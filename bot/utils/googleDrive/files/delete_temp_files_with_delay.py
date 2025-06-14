import asyncio
import shutil

from bot.config import MOCK_MODE, TEMP_FOLDER_PATH
from bot.logger import logger


# Функция для удаления временных файлов с задержкой
async def delete_temp_files_with_delay(folder_name: str, user_id: int):
    await asyncio.sleep(60 * 60)  # Ждем час
    if not MOCK_MODE:
        try:
            shutil.rmtree(
                f"{TEMP_FOLDER_PATH}\\{f'{folder_name}_{user_id}' if folder_name else ''}",
            )
        except Exception as e:
            logger.error(f"Ошибка при удалении временных файлов: {e}")
