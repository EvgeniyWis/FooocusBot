import os

# Получаем абсолютный путь к файлу
current_dir = os.path.dirname(os.path.abspath(__file__))

# Базовая папка с изображениями
base_dir = os.path.join(current_dir, "..", "..", "..", "images", "faceswap")

def read_image(filename):
    path = os.path.join(base_dir, filename)
    with open(path, "rb") as f:
        return f.read()

# Получаем путь к каждому лицу
evanoir_xo_source = read_image("evanoir.xo.jpg")
face_nika_saintclair_source = read_image("face nika_saintclair.jpg")
type_chloemay_source = read_image("type chloemay.jpg.jpeg")