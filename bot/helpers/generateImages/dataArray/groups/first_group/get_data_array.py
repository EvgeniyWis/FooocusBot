# Функция для генерации массива данных для запроса для первой группы
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


def first_group_get_data_array():
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
            "brittany_cross.xo",
            6,
            "10sDc9ypgszlwXRmD6_V_FHz_f9CIK6Rx",
            "1_20xxewMNIaO31v06yvUwn-1bKUHaNFI",
            "1UGGBVhIgTx-JooGysreAQ4MV7PPZMBor",
            """photorealistic, high quality, vibrant colors, bright lighting, skin detail, BREAK
            1girl, 18 years old, athletic, blonde hair, brown eyes, fair skin, slight smile.
            Style: realistic photo, Canon DSLR, soft daylight.""",
            [2, 3.10, -0.90, -1.10, 1.75, 0.6, 0.65, 0.80],
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
            "naomiruelle",
            23,
            "1ye6AlCgZG_TkvRwCXxArM2rDI1x6kF20",
            "1-suMtU3kX2zFR12Pchm05pmvnYQdrxYy",
            "1Bp5fPqB-rgvZe_SDblTCsetIfS-7y_HJ",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic, blonde hair, green eyes, tanned skin.
            Style: Instagram photo style, Canon DSLR, bright sunlight""",
            [2, 0.65, -0.90, -1.70, 3.7, 1.25, 1.75, 1.00],
        ),
        setting1_generate_data(
            "miahazelton.xo",
            24,
            "1uvYUlkG_A902uAmYwNWlXcqbYRo4hA07",
            "1LCR_JQEg2JIisADrnochKASReWbUCfrb",
            "18dssne4ftnQl6bwpY9QYj01UIp69HFbp",
            """photorealistic, high quality, BREAK
            1girl, 18 years old, blonde hair, green eyes, medium tan skin, smiling.""",
            [2, 3.10, -0.90, -1.70, 1.50, 0.9, 1.00, 0.40],
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
            "celinemyrren",
            28,
            "15gfR1qOglE1kWWu5oc1XpbzoHkj4idXi",
            "1BlPotHzWPwiEzE9BKQPh8vSy4vzWVVB0",
            "1vOfFUGtvfMXWAKH_f_nHIo3WdBwh1M3h",
            """photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, brown hair, huge breasts, slim waist, tan skin, plump lips, smirk, green eyes""",
            [1, 0.7, 1.9, 0, -0.15, -1.5],
        ),
        setting2_generate_data(
            "gracelowell.xo",
            29,
            "1O0oMnQj5bFzNPhJGpzwHuWIDPxlX2UJ8",
            "1T9ptTmprKmueWa9G6MKZf4x56bXQiEf0",
            "1qEiJD2I1THle_JUAIClz41eZAVht4iMs",
            """photorealistic portrait of an 18-year-old sorority girl with voluminous long blonde hair, slim waist, huge breasts, large hips, toned legs, tan skin, cute, big thin lips, smirk, bright green eyes, high quality and detail.""",
            [1, 0.7, 1.9, 0.05, -0.85, -1.5],
        ),
        setting2_generate_data(
            "valeriagomez.xo",
            30,
            "1SfIAd7S_W8RGHBatjWx3NXPpWsskZaGS",
            "18BQ8yxwk9PhZbeQMUNo2-xQjb-kO_La8",
            "1m1TxycO1m2eYADqUIv7LILlvXa33JVe7",
            """photorealistic portrait of an 18-year-old Arabian girl with voluminous long black hair, slim waist, large breasts and hips, toned legs, high tan skin, big plump lips, smirk, bright brown eyes, realistic style, high quality and detail.""",
            [1, 0.7, 3, 0.6, -0.35, -1.5],
        ),
        setting2_generate_data(
            "mileyleclair.xo",
            33,
            "1MLHRGi12Xt_QZ7qM5YFoS-Y_JiYU1YZs",
            "10Tcl469LW5fCwTjqhKMLNROB9YgIY6ON",
            "1nIU2pOpoDf3rE0T1zgxO3vcIroU2RL10",
            """photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, blonde hair, huge breasts, slim waist, tan skin, thin lips, smirk, green eyes""",
            [1, 0.7, 2.00, 1.20, -2.70, -1.50],
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
            "kaiastell",
            40,
            "1oGqVa9jV89Tu_isjKXDF17Ev4NzGCAbk",
            "1neZGiBZjrnEJiWtDCbh0-u7UIus5P8WR",
            "1NCEHcTwE1MSFpMmY35EVQjsjR1d7qZnZ",
            """photorealistic, high quality, skin detail, BREAK
            1girl, Asian, 18 years old, brown hair, medium-large breasts, slim waist, tan skin, thin lips, smirk, blue eyes""",
            [1, 0.7, 3, 1.4, -0.30, -1.5],
        ),
        setting2_generate_data(
            "kenzienoir",
            42,
            "1o55kU-E9drxz2wLEiDgxWfrGHlaoulnr",
            "1eqHguRed-ANrWjUjDdxH2GXs_CBlreCO",
            "1UOWiammfsu8kn_aFnfy9W9-SWU7KbBSD",
            "photorealistic portrait of an 18-year-old Asian girl with voluminous long ash-blonde hair, slim waist, medium saggy breasts, large hips, toned legs, tan skin, cute, big thin lips, smirk, bright blue eyes, sharp facial features and cheekbones, high quality and detail.",
            [1, 0.7, 1.6, 0.8, -0.75, -1.5, 1.1],
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
            "nicolevalaine",
            47,
            "1sZ3ea2uNlh7-kaJIVmsIRmfP5sF99tn8",
            "1RdFT0lBr10rKHDxaOLtRXtIb61l36Xiq",
            "1nDN6TK65CSAO2mjtH1NzuzfaeKoYCMle",
            """photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, ash-blonde hair, huge breasts, slim waist, tan skin, thin lips, smirk, blue eyes""",
            [1, 0.7, 2.30, 1.20, -2.35, -1.50],
        ),
    ]

    return data_array
