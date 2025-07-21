from bot.adapters.database import PostgresRepository


class UserSettingsService:
    def __init__(self, repo: PostgresRepository):
        self.repo = repo

    async def ensure_user_exists(self, user_id: int):
        user_db_id = await self.repo.get_user_db_id(user_id)
        if user_db_id is None:
            await self.repo.add_user(user_id)

    async def get_user_by_user_id(self, user_id: int):
        return await self.repo.get_user_by_user_id(user_id)

    # --- Superadmin ---

    async def superadmin_add_allowed_user(self, tg_id: int):
        return await self.repo.superadmin_add_allowed_user(tg_id)

    async def superadmin_delete_allowed_user(self, tg_id: int):
        return await self.repo.superadmin_delete_allowed_user(tg_id)

    async def superadmin_get_all_allowed_users(self):
        return await self.repo.superadmin_get_all_allowed_users()

    async def superadmin_get_current_allowed_user(self, tg_id: int):
        return await self.repo.superadmin_get_current_allowed_user(tg_id)

    async def superadmin_get_all_loras(self, setting_number: int):
        return await self.repo.superadmin_get_all_loras(setting_number)

    async def superadmin_add_lora(self, title: str, setting_number: int):
        return await self.repo.superadmin_add_lora(title, setting_number)

    async def superadmin_delete_lora(self, title: str, setting_number: int):
        return await self.repo.superadmin_delete_lora(title, setting_number)

    async def superadmin_rename_lora(
        self,
        title: str,
        setting_number: int,
        new_title: str,
    ):
        return await self.repo.superadmin_rename_lora(
            title,
            setting_number,
            new_title,
        )

    async def superadmin_get_lora_id(self, title: str, setting_number: int):
        return await self.repo.superadmin_get_lora_id(title, setting_number)

    async def get_all_setting_numbers(self) -> list[int]:
        return await self.repo.get_all_setting_numbers()

    # --- User ---

    async def user_get_loras(self, user_id: int):
        await self.ensure_user_exists(user_id)
        return await self.repo.user_get_loras(user_id)

    async def user_get_lora_weight(
        self,
        user_id: int,
        lora_id: int,
        model_id: int,
        setting_number: int,
    ):
        return await self.repo.user_get_lora_weight

    async def user_get_loras_by_setting(
        self,
        user_id: int,
        setting_number: int,
    ):
        await self.ensure_user_exists(user_id)
        return await self.repo.user_get_loras_by_setting(
            user_id,
            setting_number,
        )

    async def user_add_lora(
        self,
        user_id: int,
        lora_id: int,
        model_id: int,
        setting_number: int,
        weight: float,
    ):
        await self.ensure_user_exists(user_id)
        return await self.repo.user_add_lora(
            user_id,
            lora_id,
            model_id,
            setting_number,
            weight,
        )

    async def user_delete_lora(
        self,
        user_id: int,
        lora_id: int,
        setting_number: int,
    ):
        return await self.repo.user_delete_lora(
            user_id,
            lora_id,
            setting_number,
        )

    async def get_lora_overrides(
        self,
        user_id: int,
        lora_id: int,
        setting_number: int,
    ) -> list[dict]:
        return await self.repo.get_lora_overrides(
            user_id,
            lora_id,
            setting_number,
        )

    async def user_get_prompts(self, user_id: int):
        await self.ensure_user_exists(user_id)
        return await self.repo.user_get_prompts(user_id)

    async def user_edit_prompt(
        self,
        user_id,
        model_id,
        setting_number,
        prompt,
        prompt_type,
    ):
        return await self.repo.user_edit_prompt(
            user_id,
            model_id,
            setting_number,
            prompt,
            prompt_type,
        )

    async def user_add_prompt(
        self,
        user_id: int,
        model_id: int,
        setting_number: int,
        prompt: str,
        prompt_type: str = "positive",  # 'positive' или 'negative'
    ):
        await self.ensure_user_exists(user_id)
        return await self.repo.user_add_prompt(
            user_id,
            model_id,
            setting_number,
            prompt,
            prompt_type,
        )

    async def user_delete_prompt(
        self,
        user_id: int,
        model_id: int,
        setting_number: int,
        prompt_type: str = "positive",
    ):
        return await self.repo.user_delete_prompt(
            user_id,
            model_id,
            setting_number,
            prompt_type,
        )

    async def get_model_id(self, name: str, setting_number: int) -> int | None:
        return await self.repo.get_model_id(name, setting_number)

    async def user_update_lora_weight_delta(
        self,
        user_db_id: int,
        lora_id: int,
        model_id: int,
        setting_number: int,
        delta_weight: float,
    ):
        return await self.repo.user_update_lora_weight_delta(
            user_db_id,
            lora_id,
            model_id,
            setting_number,
            delta_weight,
        )

    async def user_get_prompt(
        self,
        user_id: int,
        model_id: int | None,
        setting_number: int | None,
        prompt_type: str = "positive",
    ):
        return await self.repo.user_get_prompt(
            user_id,
            model_id,
            setting_number,
            prompt_type,
        )

    async def user_add_lora_to_setting(
        self,
        user_id,
        lora_id,
        setting_number,
        weight,
    ):
        await self.ensure_user_exists(user_id)
        return await self.repo.user_add_lora_to_setting(
            user_id,
            lora_id,
            setting_number,
            weight,
        )

    async def user_override_lora_weight_for_model(
        self,
        user_id,
        lora_id,
        model_id,
        setting_number,
        new_weight,
    ):
        return await self.repo.user_override_lora_weight_for_model(
            user_id,
            lora_id,
            model_id,
            setting_number,
            new_weight,
        )

    async def user_delete_override_lora_weight(
        self,
        user_id,
        lora_id,
        model_id,
        setting_number,
    ):
        return await self.repo.user_delete_override_lora_weight(
            user_id,
            lora_id,
            model_id,
            setting_number,
        )
