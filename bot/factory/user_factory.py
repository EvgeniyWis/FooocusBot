from bot.adapters.database import PostgresRepository
from bot.factory.postgres_factory import get_postgres_db
from bot.services.user.user_service import UserSettingsService

_user_settings_service: UserSettingsService | None = None


async def get_user_settings_service() -> UserSettingsService:
    global _user_settings_service
    if _user_settings_service is None:
        pool = await get_postgres_db()
        repo = PostgresRepository(pool)
        _user_settings_service = UserSettingsService(repo)
    return _user_settings_service
