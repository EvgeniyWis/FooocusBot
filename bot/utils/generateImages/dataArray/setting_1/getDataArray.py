from .generateData import setting1_generateData

# Функция для генерации массива данных для запроса для настройки 1
def setting1_getDataArray():
    # Массив дат с нужными параметрами для запроса
    dataArray = [
        setting1_generateData("evanoir.xo", "1EXSJFNJFyF8TRs9zxkVcabiPqJiYVI2W", "18V64itY-c07U43aZb09mdzgVU9UGa242", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, 20 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, beautiful face, natural light on face, plump lips, realistic blue eyes, long voluminous brown hair, natural skin texture, fine pores, detailed body, subtle highlights

        Style: realistic photography, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright indirect light highlighting her features)).""",
        [2, 1.6, -0.9, -1.5, 1.5, 1.0, 1.75, 1.0, 0.35]),

        setting1_generateData("nika_saintclair", "1_vdAzRZ5dJBt1pNY-6V0b6fh31TV-12P", "1Jh4tLqkCxo4gmOw2WeWlqQuBkDB10ZB4", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, 20 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, beautiful face, natural light on face, plump lips, realistic blue eyes, long voluminous brown hair, natural skin texture, fine pores, detailed body, subtle highlights

        Style: realistic photography, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright indirect light highlighting her features)).""",
        [2, 2, -0.9, -1.5, 1.5, 1.0, 1.70, 1.0]),
    ]

    return dataArray