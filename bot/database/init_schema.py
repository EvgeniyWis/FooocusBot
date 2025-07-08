from bot.constants import BASE_DIR
from bot.factory.postgres_factory import get_postgres_db


async def init_schema():
    sql_path = BASE_DIR / "bot" / "database" / "queries.sql"
    queries = sql_path.read_text()

    pool = await get_postgres_db()

    async with pool.acquire() as conn:
        async with conn.transaction():
            for stmt in queries.split(";"):
                stmt = stmt.strip()
                if stmt:
                    await conn.execute(stmt)
