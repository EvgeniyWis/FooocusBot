from bot.helpers.generateImages.dataArray.generateLoras import generateLoras


# Функция для генерации массива лор для настройки 2
def setting2_generateLoras(weights: list[int]):
    loras = [
        "Crazy_Girlfriend_Mix.safetensors",
        "Real_Beauty.safetensors",
        "Breast_Enlargement_Slider.safetensors",
        "Big_Natural_Breasts.safetensors",
        "Body_Weight_Slider.safetensors",
        "Nipple_Size_Slider.safetensors",
        "Ass_Size_Slider.safetensors",
    ]

    return generateLoras(weights, loras)
