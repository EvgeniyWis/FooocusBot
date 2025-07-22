def validate_task_id(task_id: str):
    if not task_id or not isinstance(task_id, str):
        raise ValueError("Некорректный task_id")

def validate_base64_image(image: str):
    if not image or not isinstance(image, str):
        raise ValueError("Некорректный формат изображения (ожидается base64-строка)")
