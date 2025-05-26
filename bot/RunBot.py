from aiogram.types import BotCommand
from config import TEMP_FOLDER_PATH
from InstanceBot import bot, dp
import handlers
import asyncio
from logger import logger
import shutil
import os
from config import DEV_CHAT_ID

async def on_startup() -> None:
    # Удаляем все файлы в папке temp
    if os.path.exists(TEMP_FOLDER_PATH):
        shutil.rmtree(TEMP_FOLDER_PATH)

    # Удаляем папку temp
    if os.path.exists("FocuuusBot/temp"):
        shutil.rmtree("FocuuusBot/temp")

    # Удаляем содержимое папки results для facefusion-docker
    if os.path.exists("facefusion-docker/.assets/images/results"):
        for file in os.listdir("facefusion-docker/.assets/images/results"):
            file_path = os.path.join("facefusion-docker/.assets/images/results", file)
            if os.path.isfile(file_path):
                os.remove(file_path)

    # Создаём temp папку
    os.makedirs("FocuuusBot/temp/images", exist_ok=True)

    # Добавляем обработчики
    handlers.hand_commands.hand_add()
    handlers.hand_startGeneration.hand_add()
    handlers.hand_randomizer.hand_add()
    handlers.hand_videoGeneration.hand_add()
    
    bot_info = await bot.get_me()

    await bot.delete_webhook(drop_pending_updates=True)

    # Определяем команды и добавляем их в бота
    commands = [
        BotCommand(command='/start', description='Перезапустить бота'),
        BotCommand(command='/stop', description='Остановить генерацию'),
    ]

    await bot.set_my_commands(commands)

    logger.info(f'Бот запущен - @{bot_info.username}')

    # Отправка DEV сообщения разработчику
    await bot.send_message(DEV_CHAT_ID, "Бот запущен ✅")

    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(on_startup())
