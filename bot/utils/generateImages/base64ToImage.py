import base64
from PIL import Image
import io
from logger import logger
import os


# Функция для преобразования изображения из base64 в PIL Image
async def base64ToImage(image_data: str, folder_name: str, index: int, user_id: int, job_id: int, is_test_generation: bool) -> Image.Image:
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
        
        # Если папка не указана, то значит это тестовая генерация
        if is_test_generation:
            folder_name = "test"

        save_dir = f"temp/{folder_name}_{user_id}/{job_id}"
        os.makedirs(save_dir, exist_ok=True)
        file_path = f"{save_dir}/{index}.png"
        
        # Используем контекстный менеджер для сохранения и закрытия файла
        with open(file_path, 'wb') as f:
            image.save(f, format='PNG')  # Явно указываем формат
            image.close()  # Закрываем изображение

        logger.info(f"Изображение успешно загружено: {image}")
        
        # Возвращаем изображение
        return file_path
        
    except Exception as e:
        print(f"Ошибка при обработке изображения: {str(e)}")
