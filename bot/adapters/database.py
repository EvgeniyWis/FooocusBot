from asyncpg import Pool

from bot.logger import logger

# todo: edit_loras


class PostgresRepository:
    def __init__(self, db: Pool):
        self.db = db

    async def add_user(self, user_id: int):
        async with self.db.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO users (user_id)
                VALUES ($1)
                ON CONFLICT (user_id) DO NOTHING
                """,
                user_id,
            )
            logger.info(f"User {user_id} added to database")

    async def delete_user(self, user_id: int):
        async with self.db.acquire() as conn:
            await conn.execute("DELETE FROM users WHERE user_id = $1", user_id)
            logger.info(f"User {user_id} deleted from database")

    async def get_user_db_id(self, user_id: int) -> int | None:
        async with self.db.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id FROM users WHERE user_id = $1",
                user_id,
            )
            logger.info(f"User {user_id} fetched from database")
            return row["id"] if row else None

    async def add_lora(self, title: str):
        async with self.db.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO loras (title)
                VALUES ($1)
                ON CONFLICT (title) DO NOTHING
                """,
                title,
            )
            logger.info(f"Lora {title} added to database")

    async def delete_lora(self, title: str):
        async with self.db.acquire() as conn:
            await conn.execute("DELETE FROM loras WHERE title = $1", title)
            logger.info(f"Lora {title} deleted from database")

    async def get_lora_id_by_title(self, title: str) -> int | None:
        async with self.db.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id FROM loras WHERE title = $1",
                title,
            )
            logger.info(f"Lora {title} fetched from database")
            return row["id"] if row else None

    async def get_all_loras(self):
        async with self.db.acquire() as conn:
            logger.info("All loras fetched from database")
            return await conn.fetch("SELECT title FROM loras")

    async def add_user_lora(
        self,
        user_id: int,
        lora_id: int,
        model_name: str,
        setting_number: int,
        weight: float,
    ):
        async with self.db.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO user_loras (user_id, lora_id, model_name, setting_number, weight)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT DO NOTHING
                """,
                user_id,
                lora_id,
                model_name,
                setting_number,
                weight,
            )
            logger.info(f"User {user_id} added lora {lora_id} to database")

    async def delete_user_lora(
        self,
        user_id: int,
        lora_id: int,
        model_name: str,
        setting_number: int,
        weight: float,
    ):
        async with self.db.acquire() as conn:
            await conn.execute(
                """
                DELETE FROM user_loras
                WHERE user_id = $1 AND lora_id = $2 AND model_name = $3 AND setting_number = $4 AND weight = $5
                """,
                user_id,
                lora_id,
                model_name,
                setting_number,
                weight,
            )
            logger.info(f"User {user_id} deleted lora {lora_id} from database")

    async def get_user_loras(self, user_id: int):
        async with self.db.acquire() as conn:
            return await conn.fetch(
                "SELECT lora_id, model_name, setting_number, weight FROM user_loras WHERE user_id = $1",
                user_id,
            )
            logger.info(f"User {user_id} fetched loras from database")

    async def add_user_prompt(
        self,
        user_id: int,
        model_name: str,
        setting_number: int,
        prompt: str,
    ):
        async with self.db.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO user_prompts (user_id, model_name, setting_number, prompt)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (user_id, model_name, setting_number) DO UPDATE SET prompt = EXCLUDED.prompt
                """,
                user_id,
                model_name,
                setting_number,
                prompt,
            )
            logger.info(f"User {user_id} added prompt to database")

    async def delete_user_prompt(
        self,
        user_id: int,
        model_name: str,
        setting_number: int,
    ):
        async with self.db.acquire() as conn:
            await conn.execute(
                "DELETE FROM user_prompts WHERE user_id = $1 AND model_name = $2 AND setting_number = $3",
                user_id,
                model_name,
                setting_number,
            )
            logger.info(f"User {user_id} deleted prompt from database")

    async def get_user_prompts(self, user_id: int):
        async with self.db.acquire() as conn:
            return await conn.fetch(
                "SELECT model_name, setting_number, prompt FROM user_prompts WHERE user_id = $1",
                user_id,
            )
            logger.info(f"User {user_id} fetched prompts from database")
