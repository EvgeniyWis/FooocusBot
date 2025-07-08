import asyncpg

from bot.settings import settings

_postgres_db = None


async def get_postgres_db():
    global _postgres_db
    if _postgres_db is None:
        _postgres_db = await asyncpg.create_pool(
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            database=settings.POSTGRES_DB,
        )
    return _postgres_db
