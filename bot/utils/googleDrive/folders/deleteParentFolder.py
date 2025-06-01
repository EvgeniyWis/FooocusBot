import asyncio
import os
import shutil

from config import TEMP_FOLDER_PATH
from logger import logger


async def deleteParentFolder(folder_name: str, user_id: int):
    try:
        await asyncio.sleep(60 * 60)  # 1 час
        parent_path = f"{TEMP_FOLDER_PATH}/{folder_name}_{user_id}"
        if os.path.exists(parent_path):
            shutil.rmtree(parent_path)
    except Exception as e:
        logger.error(f"Ошибка при удалении родительской папки: {e}")
