# Функция для генерации массива данных для запроса для второй группы
from bot.helpers.generateImages.dataArray.settings.setting_1.generate_data import (
    setting1_generate_data,
)
from bot.helpers.generateImages.dataArray.settings.setting_2.generate_data import (
    setting2_generate_data,
)
from bot.helpers.generateImages.dataArray.settings.setting_3.generate_data import (
    setting3_generate_data,
)
from bot.helpers.generateImages.dataArray.settings.setting_4.generate_data import (
    setting4_generate_data,
)


def second_group_get_data_array():
    # Массив дат с нужными параметрами для запроса
    data_array = [
        # setting_1 модели
        setting1_generate_data(
            "chloemay.xo.xo",
            3,
            "1k5VoyK5pOmVLzzONNadgWGiJrXWjuUXG",
            "1BXpNVoneM0nSISQzyxsO9mG5SqzztP0t",
            "1As1OBjTIhckVo1APY0oiM_Db1HwbBhXO",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 20 years old, athletic body, brown hair, blue eyes, natural skin texture.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            [2, 2.9, -0.9, -1.7, 1.8, 0.9, 1, 0.8],
        ),
        setting1_generate_data(
            "sierravexley",
            10,
            "12bi_ufYXj71QzV1jTHTSjYmAjPr2Utky",
            "1Hcw9aO89wyw4dco86kt5RRCC-Ue8Rebo",
            "1SNri9MEsRnJz9NF3YdJdub6h2X0efssM",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, brown hair, blue eyes, tanned skin, ponytail.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            [2, 1.60, -0.90, -1.70, 2.80, 1.00, 2.65, 0.80],
        ),
        setting1_generate_data(
            "sasharoxelle",
            25,
            "1CC3xxDdpYqmDH-4Bm-HVA32EghXdgZlK",
            "1scBkcxWIWasoo84FTO2M_VVb_4bnqIYX",
            "14Q0ENXHYlVVV7Xm173D6C9oNQ_4O6jo5",
            """photorealistic, high quality, BREAK
            1girl, 18 years old, brown hair, blue eyes, tan skin, smiling.""",
            [2, 1.00, -0.90, -0.35, 2.5, 1.00, 1.60, 0.55, 1.95],
        ),
        
        # setting_2 модели
        setting2_generate_data(
            "vanessadior.xo",
            26,
            "1YpXc8m9btjYfoHD0fDbji0FpFrpruBSg",
            "17u0_0ZiKmMDO3kn7m-SKPFoWBOH59v2I",
            "16rm09bVW2eBM_3_JNne1K6wkIxku-LJp",
            """photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, ash-blonde hair, huge breasts, slim waist, tan skin, plump lips, smirk, blue eyes""",
            [1, 0.7, 2.5, 1, -1.05, -1.5],
        ),
        setting2_generate_data(
            "mari_avellin",
            37,
            "1AybFPSd6UN4Ki9JcXlrCy99_qBpOz1p-",
            "1YbLuKKgXrXrN-qRA6p8yMUwOh1x2aR42",
            "1b6OkOOxNcsWDL_o7uQws4o9V1kdHlw4o",
            """photorealistic, high quality, skin detail, BREAK
            1girl, 30 years old, ash-blonde hair, huge breasts, slim waist, tan skin, plump lips, smirk, brown eyes""",
            [1, 0.7, 1.00, -0.10, -0.60, -1.50],
        ),
        setting2_generate_data(
            "dianadelmar.xo",
            39,
            "1Ai36ERlPD65VzKyCYI29riQxmaoUfE_Z",
            "1nlVov-QS6ci0gxyxARFLx98XmpysSAGU",
            "1CeaLJFybbjJ5fY4Dl3Gmss9PxwAGuIcU",
            """photorealistic, high quality, skin detail, BREAK
            1girl, Asian, 18 years old, brown hair, medium-large breasts, slim waist, tan skin, thin lips, smirk, blue eyes""",
            [1, 0.7, 3.70, 1.35, -2.40, -1.50],
        ),
        setting2_generate_data(
            "lilith_rayne.xo",
            46,
            "14Sk-9RHb6NHFVapLqOZO_cfnvfn4fiJX",
            "1CX7jzPvTdwkJ6PeFsWXh17MPEb4Iakul",
            "1zqKil1L8WThOn1Sb_yjqcU_7dgtvIzzr",
            """photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, ash-blonde hair, huge breasts, slim waist, tan skin, thin lips, smirk, blue eyes""",
            [1, 0.7, 2.20, 1.00, -2.30, -1.50],
        ),
        setting2_generate_data(
            "carolinehazel.xo",
            51,
            "1Hdp3VL2CMzeob7qX5UVsbCn5he5-t6az",
            "1lxWDRkM5oA6_ugRHvQFUntysIUd9KGQy",
            "1lTb92NPF7sHOsYmRaDVflv7N2r1IVj3d",
            "photorealistic portrait, 18 years old, ash-blonde hair, big breasts, slim waist, tan skin, smirk, high quality.",
            [-1.50, 1.30, 0.7, 3.20, 0.45, -1.00],
        ),
        setting3_generate_data(
            "dasharomanova.xo",
            59,
            "1yalGaEVfgs9QOWHd93qfRejhnnM8Z07L",
            "19YGecBXjT0-Zs9lWgw_AV7DFTp9phAFG",
            "1movOYETVPHNZkrzadfva4REhsVJ5-mkt",
            "photorealistic portrait, 18 years old, platinum-blonde hair with black curls, huge breasts, slim waist, big bubble butt, tan skin, big lips, smirk, green eyes, high quality.",
            [-1.50, 1.30, 0.7, 2.90, 1.60, -0.85],
        ),
        setting3_generate_data(
            "zlatapavlova.xo",
            61,
            "1yfDlRMdThAacSl0WZ-DQZxxDRYFGeEqY",
            "1KY5NttoHI1ZvaRLjqsNfMp33AjhyuxM-",
            "1WadINZaETk_qE2fIeYG6Lm3iEa6VbxU6",
            "photorealistic portrait, 18 years old, platinum-blonde hair with black curls, huge breasts, slim waist, big bubble butt, tan skin, big lips, smirk, green eyes, high quality.",
            [-1.50, 1.30, 0.7, 2.00, 1.45, -1.00],
        ),
        setting3_generate_data(
            "callieroux",
            66,
            "1aWuuB7pRutNzGIKGrLuUsep7McH3OxYd",
            "1mRwEJ7Y64hQXWBkMODZ1LZgSOQ_vg66p",
            "1_p8Bh8Ad11uEXldIhqEcuqVSoFTVVH6N",
            "photorealistic portrait, 18 years old, ash-blonde hair, big breasts, slim waist, tan skin, smirk, high quality.",
            [-1.50, 1.30, 0.7, 3.65, -0.20, 0.30],
        ),
        
        # setting_4 модели
        setting4_generate_data(
            "abrilberries",
            82,
            "1aE9PT_0HGK6At3iNefEsfYyAyYIBoQdQ",
            "1Pv7mPHnhts33aikK43OhzVntB8kURiDC",
            "11B6AWrBo22EtY-Vd3kpmfP17WWewmTtf",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK 
            1girl, 18, sorority girl, black hair, short hair, medium-large natural breasts, tan skin, green eyes""",
            [2, 1.90, -1.70, 3.90, 1.00, 1.70, -0.70, 0.35],
        ),
        setting4_generate_data(
            "carmenkiss.xo",
            83,
            "1pVXZOO4g0tnGssdZDEZBvVAdDCreI7Or",
            "1wkNrb70731x45zvo7FwKscEJYCYk0-0E",
            "1k4wWqWfPwde9GdHZ8rECiQxhEIxYARCL",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK 
            1girl, 18, sorority girl, black hair, medium-large natural breasts, tan skin, green eyes""",
            [2, 1.50, -0.10, 1.70, 1.00, 1.70, -0.70, 0.35],
        ),
        setting4_generate_data(
            "marinalolita.xo",
            86,
            "1hchSQ3dpHU5ugYithqcO_HTqjVri0yLz",
            "1JthmZV1fIMvXxVCEl9HaS23Yegh0TBYK",
            "1rdOu2u2hOcqtP74kNWmb5fsYgWaLEqxO",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK 
            1girl, 18, sorority girl, black hair, medium-large natural breasts, tan skin, green eyes""",
            [2, 1.90, -0.1, 0.85, 2.00, 1.70, -0.70, 0.35],
        ),
        setting4_generate_data(
            "beatricemeltie",
            89,
            "1G4Zm21FBH-MYAE6IdyaLaChalkQAj-Od",
            "1BR5Z-y5WyYg3E-MeQt8UwF6VVYAAOug0",
            "1ASjnAtaa8DaTp9YXCX_2NWYV-DhCuB4B",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK 
            1girl, 18, sorority girl, white-black hair, medium-large natural breasts, tan skin, blue eyes""",
            [2, 0.70, -0.80, 3.05, 1.00, 1.70, -0.70, 0.35],
        ),
        setting4_generate_data(
            "ashleymoreaux.xo",
            96,
            "1jiLVZCzXLu8m4ZECwciGbZz6jhWVbBQ8",
            "1QzRyaI7FboYtdDDtycf19FX9G_7atYQN",
            "1VOSRqtGLELBE7sSxQJLKt4JD0W2Hqb4K",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK 
            1girl, 18, sorority girl, black hair, medium-large natural breasts, extra tan skin, blue eyes, smirk""",
            [2, 2.70, -1.70, 1.95, 1.00, 1.70, -0.70, 0.35, 0, 1.25],
        ),
    ]

    return data_array
