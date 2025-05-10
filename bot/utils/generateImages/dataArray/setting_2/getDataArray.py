from .generateData import setting2_generateData

# Функция для генерации массива данных для запроса для настройки 2
def setting2_getDataArray():
    # Массив дат с нужными параметрами для запроса
    dataArray = [
        setting2_generateData("""score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, 18 years old, sorority girl, voluminous ash-blonde hair, long hair, huge breasts, slim waist, sagging breasts, big bubble butt, huge ass toned legs, tan skin, skinny, cute, big lips, plump lips, smirk, blue eyes.""",
        [1, 1, 2.5, 1, -1.05, -1.5]),

        setting2_generateData("""score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, 18 years old, sorority girl, voluminous ash-blonde hair, long hair, huge breasts, slim waist, sagging breasts, big bubble butt, huge ass toned legs, tan skin, skinny, cute, big lips, plump lips, smirk, blue eyes.""",
        [1, 1, 2.85, 2.35, -1.05, -1.5]),

        setting2_generateData("""score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, 18 years old, sorority girl, voluminous brown hair, long hair, huge breasts, slim waist, erect breasts, upright breasts, big bubble butt, huge ass toned legs, tan skin, skinny, cute, big lips, plump lips, smirk, bright-green eyes.""",
        [1, 1, 2.5, 0.05, -0.15, -1.5])
    ]

    return dataArray