import os
import shutil

import bot.constants as constants
from bot.logger import logger


async def clean_temp_dirs() -> None:
    logger.info("Cleaning temp directories...")

    if os.path.exists(constants.TEMP_DIR):
        shutil.rmtree(constants.TEMP_DIR)

    if os.path.exists(constants.TEMP_IMAGE_FILES_DIR):
        shutil.rmtree(constants.TEMP_IMAGE_FILES_DIR)

    if os.path.exists(constants.FACEFUSION_RESULTS_DIR):
        for file in os.listdir(constants.FACEFUSION_RESULTS_DIR):
            file_path = os.path.join(constants.FACEFUSION_RESULTS_DIR, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    os.makedirs(
        os.path.join(constants.TEMP_IMAGE_FILES_DIR),
        exist_ok=True,
    )

    os.makedirs(
        os.path.join(constants.TEMP_VIDEOS_FILES_DIR),
        exist_ok=True,
    ) 