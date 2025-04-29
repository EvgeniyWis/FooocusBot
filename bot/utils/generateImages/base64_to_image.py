import base64
from PIL import Image
import io
from logger import logger
import os


# Функция для преобразования изображения из base64 в PIL Image
async def base64_to_image(image_data: str, folder_name: str, index: int) -> Image.Image:
    if not image_data:
        raise ValueError("Нет данных изображения для декодирования")
    
    # Удаляем префикс Data URL если он присутствует
    if image_data.startswith("data:image/"):
        image_data = image_data.split(",", 1)[1]

    # Декодируем base64 строку в бинарные данные
    try:
        padding = len(image_data) % 4
        if padding:
            image_data += '=' * (4 - padding)
        image_bytes = base64.b64decode(image_data)
        
        # Проверяем, что данные действительно являются изображением
        if not image_bytes.startswith(b'\x89PNG\r\n\x1a\n') and not image_bytes.startswith(b'\xff\xd8'):
            raise ValueError("Полученные данные не являются изображением PNG или JPEG")
        
        # Создаем изображение из бинарных данных
        image = Image.open(io.BytesIO(image_bytes))
        
        # Проверяем, что изображение было успешно загружено
        image.verify()
        image = Image.open(io.BytesIO(image_bytes))  # Открываем заново после verify
        os.makedirs("temp", exist_ok=True)
        file_path = f"temp/{folder_name}_{index}.png"
        image.save(file_path) # Сохраняем изображение в папку

        logger.info(f"Изображение успешно загружено: {image}")
        
        # Возвращаем изображение
        return file_path
        
    except Exception as e:
        print(f"Ошибка при обработке изображения: {str(e)}")
        print(f"Длина полученных данных: {len(image_data)}")
        print(f"Первые 20 символов данных: {image_data[:20]}")
