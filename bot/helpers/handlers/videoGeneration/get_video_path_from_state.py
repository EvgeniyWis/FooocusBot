from aiogram import types
from aiogram.fsm.context import FSMContext

from bot.logger import logger
from bot.utils.handlers import (
    getDataInDictsArray,
)


async def get_video_path_from_state(
    state: FSMContext,
    model_name: str,
    image_index: int | None = None,
) -> str | None:
    """
    Получает путь к видео из стейта по ключу generated_video_paths.

    Args:
        state: FSMContext - контекст состояния
        model_name: str - имя модели
        image_index: int | None - индекс изображения
        call: types.CallbackQuery | None - callback-запрос

    Returns:
        str | None - путь к видео
    """
    # Получаем данные
    state_data = await state.get_data()

    # Получаем путь к видео
    generated_video_paths = state_data.get("generated_video_paths", [])

    if image_index: 
        logger.info(
            f"Получены пути к видео: {generated_video_paths} и попытка получить путь к видео по имени модели {model_name} и индексу изображения {image_index}",
        )
        video_path = await getDataInDictsArray(
            generated_video_paths,
            model_name,
            image_index,
        )
    else:
        logger.info(
            f"Получены пути к видео: {generated_video_paths} и попытка получить путь к видео по имени модели {model_name}",
        )
        video_path = await getDataInDictsArray(
            generated_video_paths,
            model_name,
        )

    logger.info(f"Получен путь к видео для сохранения: {video_path}")

    return video_path