import asyncio
import base64
import concurrent.futures
import io
import os
from concurrent.futures import ProcessPoolExecutor

from PIL import Image, UnidentifiedImageError

import bot.constants as constants
from bot.logger import logger

executor = ProcessPoolExecutor()


def verify_and_reload_image(image_bytes):
    try:
        image = Image.open(io.BytesIO(image_bytes))
        image.verify()
        image = Image.open(io.BytesIO(image_bytes))
        return image
    except (OSError, UnidentifiedImageError, ValueError) as e:
        logger.error(f"[verify_and_reload_image] Ошибка при проверке изображения: {e}")
        raise ValueError(f"Не удалось проверить изображение: {e}")


def save_image_to_file(image_bytes, file_path):
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img.save(file_path, format="PNG")
        img.close()
    except (OSError, UnidentifiedImageError, ValueError) as e:
        logger.error(f"[save_image_to_file] Ошибка при сохранении изображения {file_path}: {e}")
        raise ValueError(f"Не удалось сохранить изображение: {e}")


async def save_image_to_file_async(image_bytes, file_path):
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
        await loop.run_in_executor(
            pool,
            save_image_to_file,
            image_bytes,
            file_path,
        )


async def base64_to_image(
    image_data: str,
    folder_name: str,
    index: int,
    user_id: int,
    is_test_generation: bool,
) -> str:
    """
    Преобразует изображение из base64 в PIL Image.

    Args:
        - image_data: строка base64, содержащая изображение
        - folder_name: имя папки для сохранения изображения на Google Drive
        - index: индекс выбранного изображения (выбирается пользователем с помощью клавиатуры)
        - user_id: ID пользователя
        - is_test_generation: флаг, указывающий, что это тестовая генерация

    Returns:
        - file_path: абсолютный путь к сохраненному изображению
    """

    if not image_data:
        raise ValueError("Нет данных изображения для декодирования")

    # Инициализируем file_path значением None для использования в except блоке
    file_path = None

    # Удаляем префикс Data URL если он присутствует
    if image_data.startswith("data:image/"):
        image_data = image_data.split(",", 1)[1]

    # Декодируем base64 строку в бинарные данные
    try:
        padding = len(image_data) % 4
        if padding:
            image_data += "=" * (4 - padding)
        image_bytes = base64.b64decode(image_data)

        # Проверяем, что данные действительно являются изображением
        if not image_bytes.startswith(
            b"\x89PNG\r\n\x1a\n",
        ) and not image_bytes.startswith(b"\xff\xd8"):
            logger.error(f"Полученные данные не являются изображением PNG или JPEG. Первые 20 байт: {image_bytes[:20]}")
            logger.error(f"Размер данных: {len(image_bytes)} байт")
            raise ValueError(
                "Полученные данные не являются изображением PNG или JPEG",
            )

        loop = asyncio.get_event_loop()
        image = await loop.run_in_executor(
            executor,
            verify_and_reload_image,
            image_bytes,
        )

        # Если папка не указана, то значит это тестовая генерация
        if is_test_generation:
            folder_name = "test"

        save_dir = f"{constants.TEMP_FOLDER_PATH}/{folder_name}_{user_id}"
        os.makedirs(save_dir, exist_ok=True)
        file_path = f"{save_dir}/{index}.jpg"

        logger.info(
            f"[base64_to_image] Сохраняем файл: {file_path} | folder_name={folder_name}, index={index}, user_id={user_id}, is_test_generation={is_test_generation}"
        )

        # Используем асинхронное сохранение, чтобы не блокировать event loop
        await save_image_to_file_async(image_bytes, file_path)
        logger.info(
            f"[base64_to_image] Изображение успешно загружено: {image} по пути {file_path}",
        )

        # Возвращаем путь к сохраненному изображению
        return file_path

    except Exception as e:
        logger.error(
            f"[base64_to_image] Ошибка при сохранении файла {file_path}: {e}"
        )
        raise
