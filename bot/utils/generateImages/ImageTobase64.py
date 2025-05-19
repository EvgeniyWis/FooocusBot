import base64
import io
from PIL import Image

# Функция для преобразования изображения в base64
def imageToBase64(image: Image.Image) -> str:
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()


