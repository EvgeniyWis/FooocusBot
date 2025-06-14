from bot.utils.generateImages.dataArray.generateLoras import generateLoras


# Функция для генерации массива лор для настройки 1
def setting1_generateLoras(weights: list[int]):
    loras = [
        "Pony_Realism_Slider.safetensors",
        "Breast_Size_Slider.safetensors",
        "Nipple_Size_Slider.safetensors",
        "Body_Weight_Slider.safetensors",
        "Breast_Enlargement_Slider.safetensors",
        "Crazy_Girlfriend_Mix.safetensors",
        "Big_Natural_Breasts.safetensors",
        "Hour_Glass_Body_By_Stable_Yogi.safetensors",
        "lighting_darkness_slider.safetensors",
    ]

    return generateLoras(weights, loras)
