import asyncio

from bot import handlers
from bot.app.config.settings import settings
from bot.app.core.logging import logger
from bot.app.instance import (
    bot,
    dp,
    redis_client,
    storage,
)
from bot.app.startup_tasks.clean_temp_dirs import clean_temp_dirs
from bot.app.startup_tasks.periodic_cleanup_task import periodic_cleanup_task
from bot.app.startup_tasks.register_commands import register_commands
from bot.helpers.generateImages.process_image_block import process_image_block
from bot.helpers.handlers.startGeneration import process_image
from bot.helpers.handlers.videoGeneration import process_video
from bot.middleware import (
    ErrorHandlingMiddleware,
    MediaGroupMiddleware,
    TextValidationMiddleware,
    UserContextMiddleware,
)
from bot.storage import get_redis_storage, init_redis_storage


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

    # Добавление middleware (UserContext должен идти раньше ErrorHandling)
    dp.message.middleware(UserContextMiddleware())
    dp.callback_query.middleware(UserContextMiddleware())
    dp.message.middleware(ErrorHandlingMiddleware())
    dp.callback_query.middleware(ErrorHandlingMiddleware())
    dp.message.middleware(MediaGroupMiddleware())
    dp.message.middleware(TextValidationMiddleware())

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
    asyncio.create_task(periodic_cleanup_task())

    await dp.start_polling(bot, skip_updates=True) 