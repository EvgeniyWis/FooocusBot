from .generateData import setting1_generateData

# Функция для генерации массива данных для запроса для настройки 1
def setting1_getDataArray():
    # Массив дат с нужными параметрами для запроса
    dataArray = [
        setting1_generateData("evanoir.xo", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, 20 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, beautiful face, natural light on face, plump lips, realistic blue eyes, long voluminous brown hair, natural skin texture, fine pores, detailed body, subtle highlights

        Style: realistic photography, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright indirect light highlighting her features)).""",
        [6.0, 1.6, -0.9, -1.5, 1.5, 1.0, 1.75, 1.0]),

        setting1_generateData("nika_saintclair", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, 20 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, beautiful face, natural light on face, plump lips, realistic blue eyes, long voluminous brown hair, natural skin texture, fine pores, detailed body, subtle highlights

        Style: realistic photography, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright indirect light highlighting her features)).""",
        [6.0, 2, -0.9, -1.5, 1.5, 1.0, 1.70, 1.0]),

        setting1_generateData("chloemay", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, 20 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, beautiful face, natural light on face, plump lips, realistic blue eyes, long voluminous brown hair, natural skin texture, fine pores, detailed body, subtle highlights

        Style: realistic photography, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright indirect light highlighting her features)).""",
        [6.0, 2.3, -0.9, -1.7, 1.8, 1.0, 1, 0.8])
    ]

    return dataArray