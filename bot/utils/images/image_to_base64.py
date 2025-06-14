import base64
import io

from PIL import Image


def image_to_base64(image: Image.Image) -> str:
    """
    Преобразует изображение в base64.

    Args:
        - image: PIL Image, изображение для преобразования

    Returns:
        - base64_image: строка base64, содержащая изображение
    """
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()
