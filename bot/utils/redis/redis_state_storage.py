import json
from typing import Any

from utils.redis.i_state_storage import IStateStorage
from utils.redis.redis_factory import get_redis_client
from logger import logger


class RedisStateStorage(IStateStorage):
    """
    Хранение произвольного состояния пользователя в Redis.
    Используется для сохранения и загрузки состояния пользователя между сессиями.
    
    Methods:
        save_state() -> None: Сохраняет состояние пользователя в Redis.
        
        load_state(): Загружает состояние пользователя из Redis.
        
        clear_state(): Очищает состояние пользователя в Redis.
    
    Attributes:
        redis_client: Redis клиент для взаимодействия с базой данных.
    """

    def __init__(self):
        self.redis_client = get_redis_client()

    async def save_state(self, user_id: str, state: dict[str, Any]) -> None:
        try:
            key = f"state:{user_id}"
            state_json = json.dumps(state)
            await self.redis.set(key, state_json)
            logger.info(f"State сохранен: {key}")
        except Exception as e:
            logger.error(f"Ошибка сохранения state в Redis: {e}")
            raise

    async def load_state(self, user_id: str) -> dict[str, Any]:
        key = f"state:{user_id}"
        data = await self.redis.get(key)
        if not data:
            return {}
        try:
            return json.loads(data)
        except Exception as e:
            logger.warning(f"Ошибка десериализации state для {user_id}: {e}")
            return {}

    async def clear_state(self, user_id: str) -> None:
        key = f"state:{user_id}"
        await self.redis.delete(key)
        logger.info(f"State очищен: {key}")
