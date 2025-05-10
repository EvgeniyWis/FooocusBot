# Глобальная функция для генерации данных для запроса
def generateData(prompt: str, loras: list[dict], advanced_params: dict, base_model_name: str, negative_prompt: str = "", embeddings: list[str] = []):
    data = {
        "input": {
            "api_name": "txt2img",
            "require_base64": True,
            "prompt": f"{', '.join(embeddings)} {prompt}",
            "loras": loras,
            "image_number": 4,
            "advanced_params": advanced_params,
            "negative_prompt": negative_prompt,
            "base_model_name": base_model_name
        }
    }
    return data