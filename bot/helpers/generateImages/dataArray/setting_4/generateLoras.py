from bot.helpers.generateImages.dataArray.generateLoras import generateLoras


# Функция для генерации массива лор для настройки 4
def setting4_generateLoras(weights: list[int]):
    loras = [
        "Pony_Realism_Slider.safetensors",
        "Breast_Size_Slider.safetensors",
        "Body_Weight_Slider.safetensors",
        "Breast_Enlargement_Slider.safetensors",
        "Hour_Glass_Body_By_Stable_Yogi.safetensors",
        "Real_Beauty.safetensors",
        "Nipple_Size_Slider.safetensors",
        "Brightness_slider.safetensors",
        "Skin_Color_Slider.safetensors",
        "Big_Natural_Breasts.safetensors",
    ]

    return generateLoras(weights, loras)
