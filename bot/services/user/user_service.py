from bot.adapters.database import PostgresRepository


class UserSettingsService:
    def __init__(self, repo: PostgresRepository):
        self.repo = repo

    async def ensure_user_exists(self, user_id: int):
        user_db_id = await self.repo.get_user_db_id(user_id)
        if user_db_id is None:
            await self.repo.add_user(user_id)

    async def get_user_loras(self, user_id: int):
        await self.ensure_user_exists(user_id)
        return await self.repo.get_user_loras(user_id)

    async def add_user_lora(
        self,
        user_id: int,
        lora_id: int,
        model_name: str,
        setting_number: int,
        weight: float,
    ):
        await self.ensure_user_exists(user_id)
        return await self.repo.add_user_lora(
            user_id,
            lora_id,
            model_name,
            setting_number,
            weight,
        )

    async def delete_user_lora(
        self,
        user_id: int,
        lora_id: int,
        model_name: str,
        setting_number: int,
        weight: float,
    ):
        return await self.repo.delete_user_lora(
            user_id,
            lora_id,
            model_name,
            setting_number,
            weight,
        )

    async def get_user_prompts(self, user_id: int):
        await self.ensure_user_exists(user_id)
        return await self.repo.get_user_prompts(user_id)

    async def add_user_prompt(
        self,
        user_id: int,
        model_name: str,
        setting_number: int,
        prompt: str,
    ):
        await self.ensure_user_exists(user_id)
        return await self.repo.add_user_prompt(
            user_id,
            model_name,
            setting_number,
            prompt,
        )

    async def delete_user_prompt(
        self,
        user_id: int,
        model_name: str,
        setting_number: int,
    ):
        return await self.repo.delete_user_prompt(
            user_id,
            model_name,
            setting_number,
        )

    async def get_all_loras(self):
        return await self.repo.get_all_loras()

    async def add_lora(self, title: str):
        return await self.repo.add_lora(title)

    async def delete_lora(self, title: str):
        return await self.repo.delete_lora(title)
