from aiogram.types import BotCommand

from bot.InstanceBot import bot


async def register_commands() -> None:
    commands = [
        BotCommand(command="/start", description="Перезапустить бота"),
        BotCommand(
            command="/stop",
            description="Остановить генерацию изображений",
        ),
    ]
    await bot.set_my_commands(commands) 