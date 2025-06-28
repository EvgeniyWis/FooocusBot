import asyncio
import shutil

import bot.constants as constants
from bot.logger import logger


async def deleteParentFolder(folder_name: str, user_id: int):
    try:
        await asyncio.sleep(60 * 60)  # 1 час
        parent_path = constants.TEMP_FOLDER_PATH / f"{folder_name}_{user_id}"
        if parent_path.exists():
            shutil.rmtree(parent_path)
    except Exception as e:
        logger.error(f"Ошибка при удалении родительской папки: {e}")
