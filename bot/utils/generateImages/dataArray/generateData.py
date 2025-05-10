# Глобальная функция для генерации данных для запроса
def generateData(prompt: str, embeddings: list[str], loras: list[dict], advanced_params: dict, negative_prompt: str):
    data = {
        "input": {
            "api_name": "txt2img",
            "require_base64": True,
            "prompt": f"{', '.join(embeddings)} {prompt}",
            "loras": loras,
            "image_number": 4,
            "advanced_params": advanced_params,
            "negative_prompt": negative_prompt
        }
    }
    return data