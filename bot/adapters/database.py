from asyncpg import Pool

from bot.logger import logger


class PostgresRepository:
    def __init__(self, db: Pool):
        self.db = db

    # --- Superadmin LoRA ---

    async def superadmin_add_lora(self, title: str, setting_number: int):
        async with self.db.acquire() as conn:
            logger.info(f"Adding LoRA: {title} (setting {setting_number})")
            await conn.execute(
                """
                INSERT INTO loras (title, setting_number)
                VALUES ($1, $2)
                ON CONFLICT (title, setting_number) DO NOTHING
                """,
                title,
                setting_number,
            )

    async def superadmin_delete_lora(self, title: str, setting_number: int):
        async with self.db.acquire() as conn:
            logger.info(f"Deleting LoRA: {title} (setting {setting_number})")
            await conn.execute(
                "DELETE FROM loras WHERE title = $1 AND setting_number = $2",
                title,
                setting_number,
            )

    async def superadmin_rename_lora(
        self,
        title: str,
        setting_number: int,
        new_title: str,
    ):
        async with self.db.acquire() as conn:
            logger.info(
                f"Renaming LoRA: {title} (setting {setting_number}) to {new_title}",
            )
            await conn.execute(
                """
                UPDATE loras
                SET title = $1
                WHERE title = $2 AND setting_number = $3
                """,
                new_title,
                title,
                setting_number,
            )

    async def superadmin_get_lora_id(
        self,
        title: str,
        setting_number: int,
    ) -> int | None:
        async with self.db.acquire() as conn:
            logger.info(f"Getting LoRA ID: {title} (setting {setting_number})")
            row = await conn.fetchrow(
                "SELECT id FROM loras WHERE title = $1 AND setting_number = $2",
                title,
                setting_number,
            )
            return row["id"] if row else None

    async def superadmin_get_all_loras(self, setting_number: int):
        logger.info(f"Getting all LoRAs for setting {setting_number}")
        async with self.db.acquire() as conn:
            return await conn.fetch(
                "SELECT title FROM loras WHERE setting_number = $1",
                setting_number,
            )

    async def get_all_setting_numbers(self):
        logger.info("Getting all setting numbers")
        async with self.db.acquire() as conn:
            return await conn.fetch(
                "SELECT DISTINCT setting_number FROM loras",
            )

    async def superadmin_add_model(
        self,
        name: str,
        setting_number: int,
    ) -> int:
        query = """
                INSERT INTO models (name, setting_number)
                VALUES ($1, $2)
                ON CONFLICT (name, setting_number) DO NOTHING
                RETURNING id; \
                """
        return await self.db.fetchval(query, name, setting_number)

    async def superadmin_rename_model(
        self,
        old_name: str,
        new_name: str,
        setting_number: int,
    ) -> None:
        query = """
                UPDATE models
                SET name = $1
                WHERE name = $2 AND setting_number = $3; \
                """
        await self.db.execute(query, new_name, old_name, setting_number)

    async def superadmin_delete_model(
        self,
        name: str,
        setting_number: int,
    ) -> None:
        query = """
                DELETE FROM models
                WHERE name = $1 AND setting_number = $2; \
                """
        await self.db.execute(query, name, setting_number)

    async def superadmin_get_models_by_setting(
        self,
        setting_number: int,
    ) -> list[dict]:
        query = """
                SELECT id, name
                FROM models
                WHERE setting_number = $1
                ORDER BY name; \
                """
        rows = await self.db.fetch(query, setting_number)
        return [dict(r) for r in rows]

    # --- User LoRA / Prompts ---

    async def user_get_lora_weight(
        self,
        user_id: int,
        lora_id: int,
        model_id: int,
        setting_number: int,
    ):
        return await self.db.fetchval(
            "SELECT weight FROM user_loras WHERE "
            "user_id = $1 AND lora_id = $2 AND model_id = $3 AND setting_number = $4",
            user_id,
            lora_id,
            model_id,
            setting_number,
        )

    async def get_model_id(self, name: str, setting_number: int) -> int | None:
        row = await self.db.fetchrow(
            "SELECT id FROM models WHERE name = $1 AND setting_number = $2",
            name,
            setting_number,
        )
        return row["id"] if row else None

    async def get_user_db_id(self, user_id: int) -> int | None:
        logger.info(f"Getting user DB ID for user {user_id}")
        async with self.db.acquire() as conn:
            row = await conn.fetchrow(
                "SELECT id FROM users WHERE user_id = $1",
                user_id,
            )
            return row["id"] if row else None

    async def add_user(self, user_id: int):
        logger.info(f"Adding user {user_id}")
        async with self.db.acquire() as conn:
            await conn.execute(
                "INSERT INTO users (user_id) VALUES ($1) ON CONFLICT DO NOTHING",
                user_id,
            )

    async def user_get_loras(self, user_id: int):
        logger.info(f"Getting LoRAs for user {user_id}")
        async with self.db.acquire() as conn:
            return await conn.fetch(
                """
                SELECT lora_id, model_name, setting_number, weight
                FROM user_loras
                WHERE user_id = $1
                """,
                user_id,
            )

    async def user_get_loras_by_setting(
        self,
        user_id: int,
        setting_number: int,
    ):
        async with self.db.acquire() as conn:
            logger.info(
                f"Getting LoRAs for user {user_id} and setting {setting_number}",
            )
            return await conn.fetch(
                """
                SELECT ul.lora_id, ul.model_id, ul.weight, m.name AS model_name
                FROM user_loras ul
                         JOIN models m ON ul.model_id = m.id
                WHERE ul.user_id = $1 AND m.setting_number = $2
                """,
                user_id,
                setting_number,
            )

    async def user_add_lora(
        self,
        user_id: int,
        lora_id: int,
        model_id: int,
        settings_number: int,
        weight: float,
    ):
        async with self.db.acquire() as conn:
            logger.info(
                f"Adding LoRA {lora_id} to user {user_id} for"
                f" model_id {model_id} for setting {settings_number} with weight {weight}",
            )
            await conn.execute(
                """
                INSERT INTO user_loras (user_id, lora_id, model_id, setting_number ,weight)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT DO NOTHING
                """,
                user_id,
                lora_id,
                model_id,
                settings_number,
                weight,
            )

    async def user_delete_lora(
        self,
        user_id: int,
        lora_id: int,
        model_id: int,
        setting_number: int,
    ):
        async with self.db.acquire() as conn:
            logger.info(
                f"Deleting LoRA {lora_id} from user {user_id} for model_id {model_id} for setting {setting_number}",
            )
            await conn.execute(
                """
                DELETE FROM user_loras
                WHERE user_id = $1 AND lora_id = $2 AND model_id = $3 AND setting_number = $4
                """,
                user_id,
                lora_id,
                model_id,
                setting_number,
            )

    async def user_get_prompts(self, user_id: int):
        async with self.db.acquire() as conn:
            logger.info(f"Getting prompts for user {user_id}")
            return await conn.fetch(
                "SELECT model_name, setting_number, prompt FROM user_prompts WHERE user_id = $1",
                user_id,
            )

    async def user_add_prompt(
        self,
        user_id: int,
        model_name: str,
        setting_number: int,
        prompt: str,
    ):
        async with self.db.acquire() as conn:
            logger.info(
                f"Adding prompt {prompt} to user {user_id} for model {model_name} and setting {setting_number}",
            )
            await conn.execute(
                """
                INSERT INTO user_prompts (user_id, model_name, setting_number, prompt)
                VALUES ($1, $2, $3, $4)
                ON CONFLICT (user_id, model_name, setting_number)
                DO UPDATE SET prompt = EXCLUDED.prompt
                """,
                user_id,
                model_name,
                setting_number,
                prompt,
            )

    async def user_delete_prompt(
        self,
        user_id: int,
        model_name: str,
        setting_number: int,
    ):
        async with self.db.acquire() as conn:
            logger.info(
                f"Deleting prompt from user {user_id} for model {model_name} and setting {setting_number}",
            )
            await conn.execute(
                """
                DELETE FROM user_prompts
                WHERE user_id = $1 AND model_name = $2 AND setting_number = $3
                """,
                user_id,
                model_name,
                setting_number,
            )

    async def user_update_lora_weight_delta(
        self,
        user_db_id: int,
        lora_id: int,
        model_id: int,
        setting_number: int,
        delta_weight: float,
    ):
        async with self.db.acquire() as conn:
            # Получаем текущий вес
            current_weight = await conn.fetchval(
                """
                SELECT weight FROM user_loras
                WHERE user_id = $1 AND lora_id = $2 AND model_id = $3 AND setting_number = $4
                """,
                user_db_id,
                lora_id,
                model_id,
                setting_number,
            )

            if current_weight is None:
                # Если нет такой записи — можно либо вставить новую, либо вернуть ошибку
                raise ValueError(
                    "LoRA не найдена для данного пользователя и модели",
                )

            new_weight = max(-10, current_weight + delta_weight)

            await conn.execute(
                """
                UPDATE user_loras
                SET weight = $5
                WHERE user_id = $1 AND lora_id = $2 AND model_id = $3 AND setting_number = $4
                """,
                user_db_id,
                lora_id,
                model_id,
                setting_number,
                new_weight,
            )
            return new_weight
