from asyncpg import Pool

from bot.logger import logger


class PostgresRepository:
    def __init__(self, db: Pool):
        self.db = db

    async def get_user_by_user_id(self, user_id: int):
        async with self.db.acquire() as conn:
            logger.info(f"Checking user in db {user_id}")
            row = await conn.fetchrow(
                "SELECT id FROM users WHERE user_id = $1",
                user_id,
            )
            if not row:
                raise ValueError(f"User with tg_id={user_id} not found")
            return row["id"]

    # --- Superadmin ---

    async def superadmin_add_allowed_user(self, tg_id: int):
        async with self.db.acquire() as conn:
            logger.info(f"Adding allowed_user: {tg_id}")
            await conn.execute(
                """
                INSERT INTO allowed_users (tg_id)
                VALUES ($1)
                ON CONFLICT (tg_id) DO NOTHING
                """,
                tg_id,
            )

    async def superadmin_delete_allowed_user(self, tg_id: int):
        async with self.db.acquire() as conn:
            logger.info(f"Deleting allowed_user: {tg_id}")
            await conn.execute(
                "DELETE FROM allowed_users WHERE tg_id = $1",
                tg_id,
            )

    async def superadmin_get_all_allowed_users(self):
        async with self.db.acquire() as conn:
            result = await conn.fetch(
                "SELECT tg_id FROM allowed_users",
            )
            logger.info(f"Getting all allowed users - {result}")
            return [row["tg_id"] for row in result]

    async def superadmin_get_current_allowed_user(self, tg_id):
        async with self.db.acquire() as conn:
            result = await conn.fetch(
                "SELECT tg_id FROM allowed_users WHERE tg_id = $1",
                tg_id,
            )
            logger.info(f"Getting info for allowed_user({tg_id}) - {result}")
            return [row["tg_id"] for row in result]

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

    async def superadmin_get_all_loras(
        self,
        setting_number: int,
    ) -> list[dict]:
        logger.info(f"Getting all LoRAs for setting {setting_number}")
        async with self.db.acquire() as conn:
            rows = await conn.fetch(
                "SELECT title FROM loras WHERE setting_number = $1",
                setting_number,
            )
            # Convert asyncpg Records to dictionaries
            return [dict(r) for r in rows]

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
            ORDER BY name;
            """
        rows = await self.db.fetch(query, setting_number)
        logger.info(
            f"Getting all models for setting {setting_number} - {rows}",
        )
        return [dict(r) for r in rows]

    # --- User LoRA / Prompts ---

    async def user_get_lora_weight(
        self,
        user_id: int,
        lora_id: int,
        model_id: int,
        setting_number: int,
    ) -> float | None:
        async with self.db.acquire() as conn:
            base_weight = await self.user_get_lora_weight(
                user_id,
                lora_id,
                model_id,
                setting_number,
            )

            if base_weight is None:
                return None

            delta_weight = await conn.fetchval(
                """
                SELECT weight FROM user_loras
                WHERE user_id = $1 AND lora_id = $2
                  AND model_id = $3 AND setting_number = $4
                  AND is_override = TRUE
                """,
                user_id,
                lora_id,
                model_id,
                setting_number,
            )

            return (
                base_weight + delta_weight
                if delta_weight is not None
                else base_weight
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
    ) -> list[dict]:
        async with self.db.acquire() as conn:
            logger.info(
                f"Getting LoRAs for user {user_id} and setting {setting_number}",
            )
            rows = await conn.fetch(
                """
                SELECT ul.lora_id, ul.model_id, ul.weight, l.title AS model_name, ul.is_override
                FROM user_loras ul
                         LEFT JOIN loras l ON ul.lora_id = l.id
                WHERE ul.user_id = $1 AND ul.setting_number = $2
                """,
                user_id,
                setting_number,
            )
            result = [dict(r) for r in rows]
            logger.info(f"Fetched user LoRAs for setting: {result}")
            return result

    async def user_get_loras(self, user_id: int) -> list[dict]:
        async with self.db.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT lora_id, model_id, setting_number, weight
                FROM user_loras
                WHERE user_id = $1
                """,
                user_id,
            )
            # Convert asyncpg Records to dictionaries
            result = [dict(r) for r in rows]
            logger.info(f"Fetched all user LoRAs: {result}")
            return result

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

    async def user_add_lora_to_setting(
        self,
        user_id: int,
        lora_id: int,
        setting_number: int,
        weight: float,
    ):
        await self.db.execute(
            """
            INSERT INTO user_loras (user_id, lora_id, model_id, setting_number, weight, is_override)
            VALUES ($1, $2, NULL, $3, $4, FALSE)
            ON CONFLICT (user_id, lora_id, model_id, setting_number)
                DO UPDATE SET weight = EXCLUDED.weight
            """,
            user_id,
            lora_id,
            setting_number,
            weight,
        )

    async def user_override_lora_weight_for_model(
        self,
        user_id: int,
        lora_id: int,
        model_id: int,
        setting_number: int,
        delta_weight: float,
    ):
        await self.db.execute(
            """
            INSERT INTO user_loras (user_id, lora_id, model_id, setting_number, weight, is_override)
            VALUES ($1, $2, $3, $4, $5, TRUE)
            ON CONFLICT (user_id, lora_id, model_id, setting_number)
                DO UPDATE SET weight = EXCLUDED.weight, is_override = TRUE
            """,
            user_id,
            lora_id,
            model_id,
            setting_number,
            delta_weight,
        )

    async def user_delete_override_lora_weight(
        self,
        user_id: int,
        lora_id: int,
        model_id: int,
        setting_number: int,
    ):
        await self.db.execute(
            """
            DELETE FROM user_loras
            WHERE user_id = $1 AND lora_id = $2 AND model_id = $3
              AND setting_number = $4 AND is_override = TRUE
            """,
            user_id,
            lora_id,
            model_id,
            setting_number,
        )

    async def get_lora_overrides(
        self,
        user_id: int,
        lora_id: int,
        setting_number: int,
    ) -> list[dict]:
        async with self.db.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT ul.model_id, m.name AS model_name, ul.weight
                FROM user_loras ul
                         LEFT JOIN models m ON ul.model_id = m.id
                WHERE ul.user_id = $1 AND ul.lora_id = $2 AND ul.setting_number = $3 AND ul.is_override = TRUE
                ORDER BY m.name
                """,
                user_id,
                lora_id,
                setting_number,
            )
            return [dict(row) for row in rows]

    async def user_delete_lora(
        self,
        user_id: int,
        lora_id: int,
        setting_number: int,
    ):
        async with self.db.acquire() as conn:
            logger.info(
                f"Deleting LoRA {lora_id} from user {user_id} for setting {setting_number}",
            )
            await conn.execute(
                """
                DELETE FROM user_loras
                WHERE user_id = $1 AND lora_id = $2 AND setting_number = $3
                """,
                user_id,
                lora_id,
                setting_number,
            )

    async def user_get_prompts(self, user_id: int):
        async with self.db.acquire() as conn:
            logger.info(f"Getting prompts for user {user_id}")
            return await conn.fetch(
                "SELECT model_id, setting_number, prompt, type FROM user_prompts WHERE user_id = $1",
                user_id,
            )

    async def user_edit_prompt(
        self,
        user_id: int,
        model_id: int | None,
        setting_number: int | None,
        prompt: str,
        prompt_type: str = "positive",
    ):
        async with self.db.acquire() as conn:
            logger.info(
                f"Editing {prompt_type} prompt {prompt} for user {user_id} "
                f"for model {model_id} and setting {setting_number}",
            )
            await conn.execute(
                """
                UPDATE user_prompts
                SET prompt = $1
                WHERE user_id = $2
                  AND model_id IS NOT DISTINCT FROM $3
                  AND setting_number IS NOT DISTINCT FROM $4
                  AND type = $5
                """,
                prompt,
                user_id,
                model_id,
                setting_number,
                prompt_type,
            )

    async def user_add_prompt(
        self,
        user_id: int,
        model_id: int | None,
        setting_number: int | None,
        prompt: str,
        prompt_type: str = "positive",  # 'positive' или 'negative'
    ):
        async with self.db.acquire() as conn:
            logger.info(
                f"Adding {prompt_type} prompt {prompt} to user {user_id} "
                f"for model {model_id} and setting {setting_number}",
            )
            await conn.execute(
                """
                INSERT INTO user_prompts (user_id, model_id, setting_number, type, prompt)
                VALUES ($1, $2, $3, $4, $5)
                ON CONFLICT (user_id, model_id, setting_number, type)
                    DO UPDATE SET prompt = EXCLUDED.prompt
                """,
                user_id,
                model_id,
                setting_number,
                prompt_type,
                prompt,
            )

    async def user_delete_prompt(
        self,
        user_id: int,
        model_id: int | None,
        setting_number: int | None,
        prompt_type: str = "positive",
    ):
        async with self.db.acquire() as conn:
            logger.info(
                f"Deleting {prompt_type} prompt from user {user_id} for model {model_id} and setting {setting_number}",
            )
            await conn.execute(
                """
                DELETE FROM user_prompts
                WHERE user_id = $1
                  AND model_id IS NOT DISTINCT FROM $2
                  AND setting_number IS NOT DISTINCT FROM $3
                  AND type = $4
                """,
                user_id,
                model_id,
                setting_number,
                prompt_type,
            )

    async def user_update_lora_weight_delta(
        self,
        user_db_id: int,
        lora_id: int,
        model_id: int | None,
        setting_number: int,
        delta_weight: float,
    ) -> float:
        async with self.db.acquire() as conn:
            if model_id is None:
                # глобальная настройка
                current_weight = await conn.fetchval(
                    """
                    SELECT weight FROM user_loras
                    WHERE user_id = $1 AND lora_id = $2 AND model_id IS NULL
                      AND setting_number = $3 AND is_override = FALSE
                    """,
                    user_db_id,
                    lora_id,
                    setting_number,
                )

                if current_weight is None:
                    raise ValueError("Глобальная LoRA не найдена.")

                new_weight = max(-10, min(10, current_weight + delta_weight))

                await conn.execute(
                    """
                    UPDATE user_loras
                    SET weight = $4
                    WHERE user_id = $1 AND lora_id = $2 AND model_id IS NULL
                      AND setting_number = $3 AND is_override = FALSE
                    """,
                    user_db_id,
                    lora_id,
                    setting_number,
                    new_weight,
                )
                return new_weight
            else:
                # override — дельта
                current_delta = await conn.fetchval(
                    """
                    SELECT weight FROM user_loras
                    WHERE user_id = $1 AND lora_id = $2 AND model_id = $3
                      AND setting_number = $4 AND is_override = TRUE
                    """,
                    user_db_id,
                    lora_id,
                    model_id,
                    setting_number,
                )

                current_delta = current_delta or 0.0
                new_delta = max(-10, min(10, current_delta + delta_weight))

                await conn.execute(
                    """
                    INSERT INTO user_loras (user_id, lora_id, model_id, setting_number, weight, is_override)
                    VALUES ($1, $2, $3, $4, $5, TRUE)
                    ON CONFLICT (user_id, lora_id, model_id, setting_number)
                        DO UPDATE SET weight = EXCLUDED.weight, is_override = TRUE
                    """,
                    user_db_id,
                    lora_id,
                    model_id,
                    setting_number,
                    new_delta,
                )
                return new_delta

    async def user_get_prompt(
        self,
        user_id: int,
        model_id: int | None,
        setting_number: int | None,
        prompt_type: str = "positive",
    ):
        async with self.db.acquire() as conn:
            logger.info(
                f"Getting {prompt_type} prompt for user {user_id} for model {model_id} and setting {setting_number}",
            )
            row = await conn.fetchval(
                """
                SELECT prompt FROM user_prompts
                WHERE user_id = $1
                  AND model_id IS NOT DISTINCT FROM $2
                  AND setting_number IS NOT DISTINCT FROM $3
                  AND type = $4
                """,
                user_id,
                model_id,
                setting_number,
                prompt_type,
            )
            logger.info(f"Prompt: {row}")
            return row
