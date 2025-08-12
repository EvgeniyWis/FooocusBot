from aiogram.types import BotCommand

from bot.app.instance import bot


async def register_commands() -> None:
    commands = [
        BotCommand(command="/start", description="Restart bot"),
        BotCommand(
            command="/stop",
            description="Stop image generation",
        ),
    ]
    await bot.set_my_commands(commands) 