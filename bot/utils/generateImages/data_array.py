import base64
import os

# Получаем абсолютный путь к файлу
current_dir = os.path.dirname(os.path.abspath(__file__))
source_path = os.path.join(current_dir, "..", "..", "static", "images", "source.png")
source = open(source_path, "rb").read()

# Функция для прибавления к изначальному промпту каждого элемента массива корневого промпта
def add_root_prompt(root_prompt: str):
    # Массив дат с нужными параметрами для запроса
    data_array = [{
        "input": {
            "api_name": "img2img2",
            "require_base64": True,
            "prompt": "one man",
            "image_prompts": [
                {
                    "cn_img": base64.b64encode(source).decode('utf-8'),
                    "cn_stop": 0.5,
                    "cn_weight": 1,
                    "cn_type": "FaceSwap"
                },
            ],
        }
    },
    {
        "input": {
            "api_name": "img2img2",
            "require_base64": True,
            "prompt": "one girl",
            "image_prompts": [
                {
                    "cn_img": base64.b64encode(source).decode('utf-8'),
                    "cn_stop": 0.5,
                    "cn_weight": 1,
                    "cn_type": "FaceSwap"
                },
            ],
        }
    }]


    for data in data_array:
        data['input']['prompt'] = data['input']['prompt'] + " " + root_prompt

    return data_array
