import base64

# Кодирование файла в base64
def encodeFileToBase64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')