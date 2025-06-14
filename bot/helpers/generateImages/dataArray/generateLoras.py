# Глобальная функция для генерации массива лор
def generateLoras(weights: list[int], loras_names: list[str]):
    loras = []
    for lora_name in loras_names:
        loras.append({"model_name": lora_name, "enabled": True})

    loras = loras[:len(weights)]
    for index, weight in enumerate(weights):
        loras[index]["weight"] = weight
    return loras
