import asyncio
import os
import shutil

import handlers
from aiogram.types import BotCommand
from helpers.generateImages import process_image_block
from helpers.handlers.startGeneration import process_image

from bot.config import (
    DEV_CHAT_IDS,
    FACEFUSION_DIR,
    FACEFUSION_RESULTS_DIR,
    TEMP_DIR,
    TEMP_FOLDER_PATH,
    TEMP_IMAGE_FILES_DIR,
    VIDEOS_TEMP_DIR,
    env_path,
)
from bot.InstanceBot import bot, dp, redis_client, storage
from bot.logger import logger
from bot.middleware import ErrorHandlingMiddleware
from bot.storage import get_redis_storage, init_redis_storage


async def on_startup() -> None:
    logger.info(f"Файл .env существует: {os.path.exists(env_path)}")
    logger.info(f"Путь к .env файлу: {env_path}")

    await init_redis_storage(redis_client)

    repo = get_redis_storage()
    repo.set_process_callback(process_image, "process_image")
    repo.set_process_callback(process_image_block, "process_image_block")
    asyncio.create_task(
        repo.recover_tasks(
            bot,
            storage,
        ),
    )

    logger.info(f"TEMP_IMAGE_FILES_DIR: {TEMP_IMAGE_FILES_DIR}")
    logger.info(f"FACEFUSION_DIR: {FACEFUSION_DIR}")
    logger.info(f"TEMP_FOLDER_PATH: {TEMP_FOLDER_PATH}")
    logger.info(f"VIDEOS_TEMP_DIR: {VIDEOS_TEMP_DIR}")
    logger.info(f"FACEFUSION_RESULTS_DIR: {FACEFUSION_RESULTS_DIR}")
    logger.info(f"TEMP_DIR: {TEMP_DIR})")

    # Удаляем все файлы в папке temp
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)

    # Удаляем папку temp бота
    if os.path.exists(TEMP_IMAGE_FILES_DIR):
        shutil.rmtree(TEMP_IMAGE_FILES_DIR)

    # Удаляем содержимое папки results для facefusion-docker
    if os.path.exists(FACEFUSION_RESULTS_DIR):
        for file in os.listdir(FACEFUSION_RESULTS_DIR):
            file_path = os.path.join(FACEFUSION_RESULTS_DIR, file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    # Создаём temp папку
    temp_path = os.path.join(TEMP_IMAGE_FILES_DIR, "images")
    os.makedirs(temp_path, exist_ok=True)

    # Добавляем обработчики
    handlers.hand_commands.hand_add()
    handlers.hand_startGeneration.hand_add()
    handlers.hand_randomizer.hand_add()
    handlers.hand_videoGeneration.hand_add()

    # Регистрируем middleware для обработки ошибок
    dp.message.middleware(ErrorHandlingMiddleware())
    dp.callback_query.middleware(ErrorHandlingMiddleware())

    bot_info = await bot.get_me()

    await bot.delete_webhook(drop_pending_updates=True)

    # Определяем команды и добавляем их в бота
    commands = [
        BotCommand(command="/start", description="Перезапустить бота"),
        BotCommand(
            command="/stop",
            description="Остановить генерацию изображений",
        ),
    ]

    await bot.set_my_commands(commands)

    logger.info(f"Бот запущен - @{bot_info.username}")

    # Отправка DEV сообщения разработчикам о запуске бота
    for DEV_CHAT_ID in DEV_CHAT_IDS:
        try:
            await bot.send_message(DEV_CHAT_ID, "Бот запущен ✅")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения разработчику: {e}")

    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(on_startup())
