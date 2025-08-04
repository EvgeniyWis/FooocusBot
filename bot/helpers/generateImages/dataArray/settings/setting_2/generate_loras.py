from bot.helpers.generateImages.dataArray.generate_loras import generate_loras


# Функция для генерации массива лор для группы 2
def setting2_generate_loras(weights: list[int]):
    loras = [
        "Crazy_Girlfriend_Mix.safetensors",
        "Real_Beauty.safetensors",
        "Breast_Enlargement_Slider.safetensors",
        "Big_Natural_Breasts.safetensors",
        "Body_Weight_Slider.safetensors",
        "Nipple_Size_Slider.safetensors",
        "Ass_Size_Slider.safetensors",
    ]

    return generate_loras(weights, loras)
