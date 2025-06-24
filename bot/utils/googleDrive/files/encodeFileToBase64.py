import base64
import aiofiles

# Кодирование файла в base64
async def encodeFileToBase64(image_path):
    async with aiofiles.open(image_path, "rb") as image_file:
        data = await image_file.read()
        return base64.b64encode(data).decode("utf-8")
