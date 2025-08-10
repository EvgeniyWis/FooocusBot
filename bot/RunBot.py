import asyncio

from bot.app.startup import on_startup

if __name__ == "__main__":
    asyncio.run(on_startup())
