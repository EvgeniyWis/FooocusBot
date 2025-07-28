import asyncio
import os
import shutil

from aiogram.types import BotCommand

import bot.constants as constants
from bot import handlers
from bot.helpers.generateImages.process_image_block import process_image_block
from bot.helpers.handlers.startGeneration import process_image
from bot.helpers.handlers.videoGeneration import process_video
from bot.InstanceBot import bot, dp, redis_client, storage
from bot.logger import logger
from bot.middleware import ErrorHandlingMiddleware, MediaGroupMiddleware
from bot.settings import settings
from bot.storage import get_redis_storage, init_redis_storage


async def clean_temp_dirs():
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


async def register_commands():
    commands = [
        BotCommand(command="/start", description="Перезапустить бота"),
        BotCommand(
            command="/stop",
            description="Остановить генерацию изображений",
        ),
    ]
    await bot.set_my_commands(commands)


async def on_startup():
    logger.info("Startup initiated")

    await init_redis_storage(redis_client)

    repo = get_redis_storage()
    repo.set_process_callback(process_image, settings.PROCESS_IMAGE_TASK)
    repo.set_process_callback(
        process_image_block,
        settings.PROCESS_IMAGE_BLOCK_TASK,
    )
    repo.set_process_callback(process_video, settings.PROCESS_VIDEO_TASK)
    if settings.RECOVERING_TASKS:
        asyncio.create_task(repo.recover_tasks(bot, storage))

    # Добавление обработчиков
    handlers.hand_commands.hand_add()
    handlers.hand_startGeneration.hand_add()
    handlers.hand_randomizer.hand_add()
    handlers.hand_nsfw_video.hand_add()
    handlers.hand_videoGeneration.hand_add()
    handlers.hand_multi_image.hand_add()
    handlers.hand_img2video.hand_add()
    handlers.hand_magnific_upscale.hand_add()

    # Добавление middleware
    dp.message.middleware(ErrorHandlingMiddleware())
    dp.callback_query.middleware(ErrorHandlingMiddleware())
    dp.message.middleware(MediaGroupMiddleware())

    await bot.delete_webhook(drop_pending_updates=True)

    await register_commands()

    bot_info = await bot.get_me()
    logger.info(f"Бот запущен - @{bot_info.username}")

    for chat_id in settings.DEV_CHAT_IDS:
        try:
            await bot.send_message(chat_id, "Бот запущен ✅")
        except Exception as e:
            logger.error(f"Ошибка при отправке сообщения разработчику: {e}")

    await clean_temp_dirs()

    # Запускаем задачу очистки временных файлов

    await dp.start_polling(bot, skip_updates=True)
