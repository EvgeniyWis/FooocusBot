from bot.helpers.generateImages.dataArray.extra_setting.generate_data import (
    extra_setting_generate_data,
)


# Функция для генерации массива данных для запроса для экстра-настройки
def extra_setting_get_data_array():
    # Массив дат с нужными параметрами для запроса
    data_array = [
        extra_setting_generate_data(
            "isla_latina",
            "1jAhxM40JhmvMrlFQyN-CBnfzIZYkFimT",
            "1JM0RoVqEV5K0sPwx9z1G54u_2kqjLEjG",
            "",
            [0.55, 1.7, -0.3, 0.75, 0.7, 2.25, 0.05, 0.65],
            negative_prompt="score_6, score_5, score_4, score_3, score_2, score_1, low quality, worst quality, low resolution, jpeg artifacts, blurry, out of focus, distorted, deformed, noisy image, compression artifacts, oversaturated, undersaturated, grainy, pixelated, bad lighting, poorly drawn, bad anatomy, (((penis))), (((dick))), inaccurate anatomy, extra limbs, extra arms, extra legs, missing limbs, fused limbs, mutated hands, malformed fingers, long neck, short neck, cloned face, disfigured, gross proportions, unnatural body, ugly, blurry eyes, cross-eyed, lazy eye, wrong hands, unnatural hands, extra fingers, missing fingers, fused fingers, multiple heads, low detail, lack of detail, poorly rendered, unrealistic skin, smudged skin texture, bad proportions, bad perspective, wrong shadows, out of frame, watermark, text, signature, logo, cropped head, cropped limbs, tattoo, tattooed skin, writing on skin,  mosaic blur, text overlay, bad face, wrong face, out of context,"
        ),
    ]

    return data_array
