from config import MOCK_MODE

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

        setting1_generateData("chloemay", "1FjpHnhtLUkP_e-MzsYAUb7xxBdL0Y07y", "1s6UGZKSvV5kKu1BqBTnNZOdufttz-kDK", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, 20 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, beautiful face, natural light on face, plump lips, realistic blue eyes, long voluminous brown hair, natural skin texture, fine pores, detailed body, subtle highlights

        Style: realistic photography, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright indirect light highlighting her features)).""",
        [2, 2.3, -0.9, -1.7, 1.8, 1.0, 1, 0.8]),

        setting1_generateData("arialennix", "1h8FgVo6gvJTkqCvMzMWDGQ5tSZWE5l2Y", "1pBRsAHcvCSBaeTpjCU173Y_jUnx_KY4S", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, 20 years old, skinny body, soft curves, medium teardrop-shaped breasts, toned abdomen, beautiful face, natural light on face, plump lips, realistic brown eyes, long voluminous black hair, natural skin texture, fine pores, detailed body, subtle highlights, slightly smiling, (the face is well lit by daylight).

        Style: realistic photography, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright indirect light highlighting her features)).""",
        [2, 1.20, -0.90, -1.70, 1.70, 1.00, 1.00, 0.80]),

        setting1_generateData("miaroxelle", "1QA3QAE9VYTYHFqBNi5YLtVvGQxnHJazX", "1FFCq-hoNCSzDGqeCWB6VU_Z9a-f5oaCU", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, asian, 18 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, beautiful face, natural light on face, plump lips, realistic brown eyes, long voluminous blonde hair, white skin, natural skin texture, fine pores, detailed body, subtle highlights, slightly smiling, ((the face is well lit by daylight)).

        Style: realistic photography, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright indirect light highlighting her features)).""",
        [2, 2.50, -0.90, -1.10, 1.00, 1.00, 1.00, 0.80]),

        setting1_generateData("brittany_cross.xo", "1d1LhaBIKzerdr2mbiFmlTH1uHQjTChDV", "1EZFKJf-okEGIdpy1iu62acPSOBL8Ksx6", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, caucasian, 18 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, beautiful face, natural light on face, plump lips, realistic brown eyes, long voluminous blonde hair, tanned skin, natural skin texture, fine pores, detailed body, subtle highlights, slightly smiling, ((the face is well lit by daylight)).

        Style: realistic photography, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright indirect light highlighting her features)).""",
        [2, 2.50, -0.90, -1.10, 1.75, 1.00, 0.65, 0.80]),

        setting1_generateData("zoe_callahan", "1rXaMeo6QmaZ0J81e96gjITC8LNCzqEfA", "1jX67SwRFu0L191-CT_WAHWg999QVuDcC", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, caucasian, 18 years old, athletic body, soft curves, small teardrop-shaped breasts, toned abdomen, beautiful face, natural light on face, plump lips, realistic brown eyes, long voluminous blonde hair, tanned skin, natural skin texture, fine pores, detailed body, subtle highlights, slightly smiling, ((the face is well lit by daylight)).

        Style: realistic photography, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright indirect light highlighting her features)).""",
        [2, 2.05, -0.90, -0.85, 1.40, 1.00, 1.00, 0.80]),

        setting1_generateData("brookenixon.xo", "18SDti6Kw2vmpfAc7vp8qjFxuNMKJpZFM", "1LeLF_NVSmjrKHuxS6sg6jwZfDwDUKfBD", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, caucasian, 18 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, beautiful face, natural light on face, plump lips, realistic brown eyes, long voluminous blonde hair, tanned skin, natural skin texture, fine pores, detailed body, subtle highlights, slightly smiling, ((the face is well lit by daylight)).

        Style: realistic photography, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright indirect light highlighting her features)).""",
        [2, 1.00, -0.90, -0.85, 1.80, 1.00, 0.54, 0.80]),

        setting1_generateData("giablake.xo", "1HQqiAIFC9o43hgeCQg2OKxaw70p-_ShT", "1PGOqC0qFNCsj35arZnz1iTMR6PItusrM", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, caucasian, 18 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, beautiful face, natural light on face, plump lips, realistic blue eyes, long voluminous brown hair, ((ash-white skin)), natural skin texture, fine pores, detailed body, subtle highlights, slightly smiling, ((the face is well lit by daylight)).

        Style: realistic photography, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright indirect light highlighting her features)).""",
        [2, 1.50, -0.90, -1.70, 1.60, 1.00, 1.00, 0.50]),

        setting1_generateData("sierravexley", "1NqIu4OG2U9MYAeBiI1wmYTiipHZ1yB88", "1tc3Rl0aNCWobdV-0TOL4oqv7bW0taZYD", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, caucasian, 18 years old, athletic body, soft curves, small teardrop-shaped breasts, toned abdomen, beautiful skinny face, natural light on face, plump lips, realistic blue eyes, long voluminous brown hair, tanned skin, natural skin texture, fine pores, detailed body, subtle highlights, slightly smiling, ((the face is well lit by daylight)), hair tied back in a ponytail""",
        [2, 1.00, -0.90, -1.70, 3.00, 1.00, 2.65, 0.80]),

        setting1_generateData("roxie_foxx.xo", "1IrbjKpj9tfWXV4D0ix21_zwtm_YRwK7m", "1qlSKVih-lQYD_HuVwNA8hkjZtRgwISKP", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, caucasian, 18 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, beautiful face, natural light on face, plump lips, realistic brown eyes, long voluminous blonde hair, tanned skin, natural skin texture, fine pores, detailed body, subtle highlights, slightly smiling, ((the face is well lit by daylight)), hips, hourglass body.""",
        [2, 1.00, -0.90, -1.70, 1.75, 1.00, 0.00, 0.80]),

        setting1_generateData("auroravaux.xo", "1OAgkrvbbOLsTHCjglsa_mFWU2W5jR5-2", "1a7GH8lNnzAUw6MAoSehG2euNxiRpn2EK", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, caucasian, 18 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, beautiful face, plump lips, realistic brown eyes, long voluminous blonde hair, tanned skin, natural skin texture, fine pores, detailed body, subtle highlights, slightly smiling, ((the face is well lit by bright sunlight)), hips, hourglass body.

        Style: Instagram photo style, vibrant and warm filter, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright, direct sunlight creating warm highlights and accentuating features)), bright sun light from window to body. """,
        [2, 0.10, -0.90, -1.70, 3.00, 1.00, 1.80, 0.80]),

        setting1_generateData("skylalure", "1VOIxoZOEu94vO60v7RORYwXxwmYNyVRt", "1tOtCWNhS4HSNoXeql7TUe4ZPwSIO-lWD", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, caucasian, 18 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, beautiful face, plump lips, realistic blue eyes, long voluminous blonde hair, tanned skin, natural skin texture, fine pores, detailed body, subtle highlights, slightly smiling, ((the face is well lit by bright sunlight)), hips, hourglass body.

        Style: Instagram photo style, vibrant and warm filter, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright, direct sunlight creating warm highlights and accentuating features))""",
        [2, 3.55, -0.90, -1.50, 0.45, 1.00, 0.05, 0.80]),

        setting1_generateData("zara_devaux", "1QYyGlr2Axwj-Lf_oYmYxEL3pT7S5KtvP", "1WzxkWVgXGAkPcjIYDiCqrvel8O3ERsxw", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, caucasian, 18 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, ((very narrow waist)), ((wide hips)), thin legs, beautiful face, plump lips, realistic blue eyes, long voluminous blonde hair, tanned skin, natural skin texture, fine pores, detailed body, subtle highlights, slightly smiling, ((the face is well lit by bright sunlight)), hips, hourglass body.

        Style: Instagram photo style, vibrant and warm filter, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright, direct sunlight creating warm highlights and accentuating features)), bright sunlight from outdoor courtyard on body.""",
        [2, 2.00, -0.90, -0.60, 0.45, 1.00, 0.95, 1.00]),

        setting1_generateData("alinaquinn.xo", "1277BpUC7Sb9EaZvpmDStiip1iJOep0-7", "1T7aqL4auHdBOjxzbrHlIxQypIIqOT9Xg", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, caucasian, 18 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, ((very narrow waist)), ((wide hips)), thin legs, beautiful face, plump lips, realistic blue eyes, long voluminous blonde hair, tanned skin, natural skin texture, fine pores, detailed body, subtle highlights, slightly smiling, ((the face is well lit by bright sunlight)), ((big wide hips)), hourglass body.

        Style: Instagram photo style, vibrant filter, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright, direct sunlight creating warm highlights and accentuating features)), sunlight from outdoor courtyard.""",
        [2, 2.00, -0.90, -1.70, 1.50, 1.00, 1.50, 1.00]),

        setting1_generateData("noavexen", "1GNNlKjZc32alF8CGaXWiq4S_O4-7O4Jl", "1pdmPKtEchDfSoSxFwFa3exVGj2xFg0WO", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, caucasian, 18 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, ((very narrow waist)), ((wide hips)), thin legs, beautiful face, thin lips, realistic green eyes, long voluminous brown hair, tanned skin, natural skin texture, fine pores, detailed body, subtle highlights, slightly smiling, ((the face is well lit by bright sunlight)), ((big wide hips)), hourglass body.

        Style: Instagram photo style, vibrant filter, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright, direct sunlight creating warm highlights and accentuating features)), sunlight from outdoor courtyard, ((((bright lightning face))))""",
        [2, 1.00, -0.90, -1.70, 1.55, 1.00, 3.00, 1.00]),

        setting1_generateData("lexalennix", "1ep2RT3ZoxgcLYbkFS_3Vepnk8QWRhbNO", "1ZkLEJe88qTbY-VkHFrPCv94VWMYoBEtO", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, caucasian, 18 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, ((very narrow waist)), ((wide hips)), thin legs, beautiful face, thin lips, realistic green eyes, long voluminous ((brunette)) hair, tanned skin, natural skin texture, fine pores, detailed body, subtle highlights, slightly smiling, ((the face is well lit by bright sunlight)), ((big wide hips)), hourglass body.

        Style: Instagram photo style, vibrant filter, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright, direct sunlight creating warm highlights and accentuating features)), sunlight from outdoor courtyard, ((((bright lightning face))))""",
        [2, 1.10, -0.90, -0.95, 0.95, 1.00, 0.05, 0.40]),

        setting1_generateData("gia_prescott.xo", "1IXAJLMMYPg4K9Rp0XAQYDK8zfkrGEfO8", "1tVFwpxQoX7YQbVat-8MPbxOd-Vadw5rO", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, caucasian, 18 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, ((very narrow waist)), ((wide hips)), thin legs, beautiful face, thin lips, realistic green eyes, long voluminous ((brunette)) hair, tanned skin, natural skin texture, fine pores, detailed body, subtle highlights, slightly smiling, ((the face is well lit by bright sunlight)), ((big wide hips)), hourglass body.

        Style: Instagram photo style, vibrant filter, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright, direct sunlight creating warm highlights and accentuating features)), sunlight from outdoor courtyard, ((((bright lightning face))))""",
        [2, 1.10, -0.90, 1.40, 0.95, 1.00, 0.05, 0.80]),

        setting1_generateData("daisyknoxen", "1EZoK9Z6hrpCofFZ52sWjERifm5iYegfN", "1kOAC0Sg-fleBBo7elPpKFqzxS1ad21Ua", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, redhead, caucasian, 18 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, ((very narrow waist)), ((wide hips)), thin legs, beautiful face, plump lips, realistic blue eyes, long voluminous ginger hair, tanned skin, natural skin texture, fine pores, detailed body, subtle highlights, slightly smiling, ((the face is well lit by bright sunlight)), big wide hips, hourglass body.

        Style: Instagram photo style, vibrant filter, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright, direct sunlight creating warm highlights and accentuating features)), sunlight from outdoor courtyard.""",
        [2, 2.00, -0.90, -1.70, 0.05, 1.00, 4.85, 1.00]),

        setting1_generateData("selinavoux", "1Imjgv4Mxj3tK97sOl9dYgWSFqvN9AP8e", "1zr_yKtg6i2DRuDceRos5rUJq2Gc92SPE", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, caucasian, 18 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, ((very narrow waist)), ((wide hips)), thin legs, beautiful face, thin lips, realistic green eyes, long voluminous black hair, (((extra-white skin tone))), natural skin texture, fine pores, detailed body, subtle highlights, slightly smiling, ((the face is well lit by bright sunlight)), ((big wide hips)), hourglass body.

        Style: Instagram photo style, vibrant filter, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright, direct sunlight creating warm highlights and accentuating features)), sunlight from outdoor courtyard, ((((bright lightning face))))""",
        [2, 2.05, -0.90, -0.25, 0.70, 1.00, 0.10, 0.75]),

        setting1_generateData("thaliavonn", "1TYAOuThV7x0yRDq3KA6i7phVw4ccJ22P", "1YMADcvWKAn3QblIBo3siSmafEIHaYgXv", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, caucasian, 18 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, ((very narrow waist)), ((wide hips)), thin legs, beautiful face, plump lips, realistic blue eyes, long voluminous blonde hair, tanned skin, natural skin texture, fine pores, detailed body, subtle highlights, slightly smiling, ((the face is well lit by bright sunlight)), big wide hips, hourglass body.

        Style: Instagram photo style, vibrant filter, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright, direct sunlight creating warm highlights and accentuating features)), sunlight from outdoor courtyard.""",
        [2, 0.50, -0.90, 0.35, 1.70, 1.00, 0.95, 1.00]),

        setting1_generateData("adelinedior", "15sxf1borQ55h9YgAzTGv7SuJdgas5wwW", "12jyke3mZadunB52QEWnkSEAZSYd1IDMG", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, caucasian, 18 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, ((very narrow waist)), ((wide hips)), thin legs, beautiful face, plump lips, realistic blue eyes, long voluminous blonde hair, tanned skin, natural skin texture, fine pores, detailed body, subtle highlights, slightly smiling, ((the face is well lit by bright sunlight)), big wide hips, hourglass body.

        Style: Instagram photo style, vibrant filter, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright, direct sunlight creating warm highlights and accentuating features)), sunlight from outdoor courtyard.""",
        [2, 1.15, -0.90, -1.70, 0.10, 1.00, 0.10, 1.00]),

        setting1_generateData("naomiruelle", "1gn66CiTa7zOIKlEfn7bWc3P4jKcT_3B2", "1CUO8t2lTITorGZGg3U3PJ-7ZpcagZU5l", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, caucasian, 18 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, ((very narrow waist)), ((wide hips)), ((extra-skinny girl with big boobs)), thin legs, beautiful face, plump lips, realistic green eyes, long voluminous blonde hair, tanned skin, natural skin texture, fine pores, detailed body, subtle highlights, slightly smiling, ((the face is well lit by bright sunlight)), big wide hips, hourglass body.

        Style: Instagram photo style, vibrant filter, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright, direct sunlight creating warm highlights and accentuating features)), sunlight from outdoor courtyard.""",
        [2, 0.05, -0.90, -1.70, 3.65, 1.00, 1.75, 1.00]),

        setting1_generateData("miahazelton.xo", "1TlI9UYahiPAhtCKj9XNySgX5SEw7igoT", "1WtNip-zF8TcZxkofOh_dCuYNGzE8rqVy", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, caucasian, 18 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, ((very narrow waist)), ((wide hips)), ((extra-skinny girl with big boobs)), thin legs, beautiful face, plump lips, realistic green eyes, long voluminous blonde hair, tanned skin, natural skin texture, fine pores, detailed body, subtle highlights, slightly smiling, ((the face is well lit by bright sunlight)), big wide hips, hourglass body.

        Style: Instagram photo style, vibrant filter, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright, direct sunlight creating warm highlights and accentuating features)), sunlight from outdoor courtyard.""",
        [2, 2.50, -0.90, -1.70, 1.50, 1.00, 1.00, 0.40]),

        setting1_generateData("sasharoxelle", "1tgnt_OF_1LRV906o6SZ8oNrra_fP537x", "1VNp7H97nJHl5CXxl8ytNehP8vXj_AiId", """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

        real_beauty, igbaddie, 1girl, caucasian, 18 years old, athletic body, soft curves, medium teardrop-shaped breasts, toned abdomen, ((very narrow waist)), ((wide hips)), ((extra-skinny girl with big boobs)), thin legs, beautiful face, plump lips, realistic blue eyes, long straight brown hair, ponytail hair, tanned skin, natural skin texture, fine pores, detailed body, subtle highlights, slightly smiling, ((the face is well lit by bright sunlight)), big wide hips, hourglass body.

        Style: Instagram photo style, vibrant filter, high-resolution, Canon DSLR simulation, shallow depth of field, soft natural daylight, ((bright, direct sunlight creating warm highlights and accentuating features))

lighting: ((bright daylight, model fully illuminated, photo bright, maximally illuminated))""",
        [2, 0.40, -0.90, -0.35, 2.10, 1.00, 1.60, 0.55, 1.95]),
    ]

    if MOCK_MODE:
        dataArray = dataArray[:1]

    return dataArray
