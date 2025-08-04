from bot.helpers.generateImages.dataArray.generate_loras import generate_loras


# Функция для генерации массива лор для группы 3
def setting3_generate_loras(weights: list[int]):
    loras = [
        "Nipple_Size_Slider.safetensors",
        "Crazy_Girlfriend_Mix.safetensors",
        "Real_Beauty.safetensors",
        "Breast_Enlargement_Slider.safetensors",
        "Big_Natural_Breasts.safetensors",
        "Body_Weight_Slider.safetensors",
    ]

    return generate_loras(weights, loras)
