from aiogram.types import BotCommand
from config import TEMP_FOLDER_PATH
from InstanceBot import bot, dp
import handlers
import asyncio
from logger import logger
import shutil
import os

async def on_startup() -> None:
    # Удаляем все файлы в папке temp
    if os.path.exists(TEMP_FOLDER_PATH):
        shutil.rmtree(TEMP_FOLDER_PATH)

    # Удаляем папку temp
    if os.path.exists("FocuuusBot/temp"):
        shutil.rmtree("FocuuusBot/temp")

    handlers.hand_start.hand_add()
    
    bot_info = await bot.get_me()

    await bot.delete_webhook(drop_pending_updates=True)

    # Определяем команды и добавляем их в бота
    commands = [
        BotCommand(command='/start', description='Перезапустить бота'),
        BotCommand(command='/stop', description='Остановить генерацию'),
    ]

    await bot.set_my_commands(commands)

    logger.info(f'Бот запущен - @{bot_info.username}')

    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(on_startup())
