from bot.helpers.generateImages.dataArray.generate_loras import generate_loras


# Функция для генерации массива лор для экстра-настройки
def extra_setting_generate_loras(weights: list[int]):
    loras = [
        "Pony_Amateur.safetensors",
        "Breast_Size_Slider.safetensors",
        "Nipple_Size_Slider.safetensors",
        "Real_Beauty.safetensors",
        "Ass_Size_Slider.safetensors",
        "Pony_Realism_Slider.safetensors",
        "Rawfully_Stylish.safetensors",
        "Crazy_Girlfriend_Mix.safetensors",
    ]

    return generate_loras(weights, loras)
