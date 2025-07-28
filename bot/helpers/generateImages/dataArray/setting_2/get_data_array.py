from bot.helpers.generateImages.dataArray.setting_2.generate_data import (
    setting2_generate_data,
)


# Функция для генерации массива данных для запроса для настройки 2
def setting2_get_data_array():
    # Массив дат с нужными параметрами для запроса
    dataArray = [
        setting2_generate_data(
            "vanessadior.xo",
            "1YpXc8m9btjYfoHD0fDbji0FpFrpruBSg",  # picture
            "17u0_0ZiKmMDO3kn7m-SKPFoWBOH59v2I",  # video
            "16rm09bVW2eBM_3_JNne1K6wkIxku-LJp",  # nsfw_video
            """photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, ash-blonde hair, huge breasts, slim waist, tan skin, plump lips, smirk, blue eyes""",
            [1, 0.7, 2.5, 1, -1.05, -1.5],
        ),
        setting2_generate_data(
            "cleawynn",
            "1EVxSMsbIpfv5jzdHzKJHf_-gvVyU6tVl",  # picture
            "12NVZqcKKY7TF-uKdgyI7tPJeIIJHLWuk",  # video
            "1qw0jYfb6_ScvkNEGkvLkc86qxKxeUcjc",  # nsfw_video
            """photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, ash-blonde hair, huge breasts, slim waist, tan skin, plump lips, smirk, blue eyes""",
            [1, 0.7, 1.60, -0.20, -0.95, -1.50],
        ),
        setting2_generate_data(
            "celinemyrren",
            "15gfR1qOglE1kWWu5oc1XpbzoHkj4idXi",  # picture
            "1BlPotHzWPwiEzE9BKQPh8vSy4vzWVVB0",  # video
            "1vOfFUGtvfMXWAKH_f_nHIo3WdBwh1M3h",  # nsfw_video
            """photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, brown hair, huge breasts, slim waist, tan skin, plump lips, smirk, green eyes""",
            [1, 0.7, 1.9, 0, -0.15, -1.5],
        ),
        setting2_generate_data(
            "gracelowell.xo",
            "1O0oMnQj5bFzNPhJGpzwHuWIDPxlX2UJ8",  # picture
            "1T9ptTmprKmueWa9G6MKZf4x56bXQiEf0",  # video
            "1qEiJD2I1THle_JUAIClz41eZAVht4iMs",  # nsfw_video
            """photorealistic portrait of an 18-year-old sorority girl with voluminous long blonde hair, slim waist, huge breasts, large hips, toned legs, tan skin, cute, big thin lips, smirk, bright green eyes, high quality and detail.""",
            [1, 0.7, 1.9, 0.05, -0.85, -1.5],
        ),
        setting2_generate_data(
            "valeriagomez.xo",
            "1SfIAd7S_W8RGHBatjWx3NXPpWsskZaGS",  # picture
            "18BQ8yxwk9PhZbeQMUNo2-xQjb-kO_La8",  # video
            "1m1TxycO1m2eYADqUIv7LILlvXa33JVe7",  # nsfw_video
            """photorealistic portrait of an 18-year-old Arabian girl with voluminous long black hair, slim waist, large breasts and hips, toned legs, high tan skin, big plump lips, smirk, bright brown eyes, realistic style, high quality and detail.""",
            [1, 0.7, 2.50, 0.55, -0.35, -1.5],
        ),
        setting2_generate_data(
            "ivyxhart",
            "1ZnKFB8d0Az0SpwtQ3sf9wvUT7qT-DSix",  # picture
            "1VGJv2-nLkoifyIJ9aHqBbW1v60hLAAGr",  # video
            "1P4g_sVOVH2__jF3jufytEypCgvZ_M350",  # nsfw_video
            """photorealistic, high quality, skin detail, BREAK
            1girl, Arabian, 18 years old, black hair, huge breasts, slim waist, tan skin, plump lips, smirk, brown eyes""",
            [1, 0.7, 2.80, 1.2, -1.90, -1.5],
        ),
        setting2_generate_data(
            "ellamaddix.xo",
            "1LK_kVSxWf9tjEr8MsUrJNHNruj0zDHJa",  # picture
            "1BXhqCls1hdM7VX134RYcaHKp2KqbsxBm",  # video
            "1XODeAySCQEEhp4iEvt-PAkUdKEwipplL",  # nsfw_video
            """photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, blonde hair, huge breasts, slim waist, tan skin, thin lips, smirk, green eyes""",
            [1, 0.7, 0.40, 0.50, -0.95, -1.50],
        ),
        setting2_generate_data(
            "mileyleclair.xo",
            "1MLHRGi12Xt_QZ7qM5YFoS-Y_JiYU1YZs",  # picture
            "10Tcl469LW5fCwTjqhKMLNROB9YgIY6ON",  # video
            "1nIU2pOpoDf3rE0T1zgxO3vcIroU2RL10",  # nsfw_video
            """photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, blonde hair, huge breasts, slim waist, tan skin, thin lips, smirk, green eyes""",
            [1, 0.7, 2.00, 1.20, -2.70, -1.50],
        ),
        setting2_generate_data(
            "thea_azelle",
            "14qTxRRP-qU8Vd720KXj1H77kUBcqnjnL",  # picture
            "1vTcIfFBFY7g7xzTFrX88MPFOoDg6xZt7",  # video
            "1sN3iwvcEHhN4bVapS2hqvMYTuJXLDBId",  # nsfw_video
            """photorealistic, high quality, skin detail, BREAK
            1girl, 30 years old, ash-blonde hair, huge breasts, slim waist, tan skin, plump lips, smirk, brown eyes""",
            [1, 0.7, 1.00, 0.30, -1.20, -1.50],
        ),
        setting2_generate_data(
            "briaclaire.xo",
            "18IdLBfKEdiKRxAuosh9SFHlt_4wlx0LC",  # picture
            "1AukiYgkiGx66rm3MjE9lFRD3Dn53S7PA",  # video
            "1UzFJhvzAi_bLNSyn8tXAzV3kAjfm_R7I",  # nsfw_video
            """photorealistic portrait of an 18-year-old sorority girl with voluminous long brown hair, slim waist, medium breasts, large hips, toned legs, tan skin, cute, big thin lips, smirk, bright blue eyes, high quality and detail.""",
            [1, 0.7, 4.00, 0.50, -1.70, -1.5],
        ),
        setting2_generate_data(
            "rinazuri.xo",
            "1l-3_6TZ-UYCHlvu84ehRrWN0X9Qj_I-k",  # picture
            "1pTlBMtlJvF4RvK1FdPHqc2W31Rhx0WC_",  # video
            "1u3SoUQVlurTPHfQA5coZdKcn-Wt3iveT",  # nsfw_video
            "photorealistic portrait of an 18-year-old girl with ash-blonde hair, slim figure, tan skin, blue eyes, slight smile, soft natural light, high detail.",
            [1, 0.7, 3.10, 0.30, -0.80, -1.50],
        ),
        setting2_generate_data(
            "mari_avellin",
            "1AybFPSd6UN4Ki9JcXlrCy99_qBpOz1p-",  # picture
            "1YbLuKKgXrXrN-qRA6p8yMUwOh1x2aR42",  # video
            "1b6OkOOxNcsWDL_o7uQws4o9V1kdHlw4o",  # nsfw_video
            """photorealistic, high quality, skin detail, BREAK
            1girl, 30 years old, ash-blonde hair, huge breasts, slim waist, tan skin, plump lips, smirk, brown eyes""",
            [1, 0.7, 1.00, -0.10, -0.60, -1.50],
        ),
        setting2_generate_data(
            "amirawellex",
            "1JcFuppimxi7kfIvJf45D5S951mBkMpzU",  # picture
            "13Hz2l5tM361tUItIOLpLdfLozYpv3Lca",  # video
            "14GDeOofD6vMg8gEIxhbwSx93r2b_gv1D",  # nsfw_video
            """photorealistic, high quality, skin detail, BREAK
            1girl, Asian, 18 years old, black hair, medium-large breasts, slim waist, tan skin, thin lips, smirk, blue eyes""",
            [1, 0.7, 2.75, 0.15, -1.30, -1.5],
        ),
        setting2_generate_data(
            "dianadelmar.xo",
            "1Ai36ERlPD65VzKyCYI29riQxmaoUfE_Z",  # picture
            "1nlVov-QS6ci0gxyxARFLx98XmpysSAGU",  # video
            "1CeaLJFybbjJ5fY4Dl3Gmss9PxwAGuIcU",  # nsfw_video
            """photorealistic, high quality, skin detail, BREAK
            1girl, Asian, 18 years old, brown hair, medium-large breasts, slim waist, tan skin, thin lips, smirk, blue eyes""",
            [1, 0.7, 3.70, 1.35, -2.40, -1.50],
        ),
        setting2_generate_data(
            "kaiastell",
            "1oGqVa9jV89Tu_isjKXDF17Ev4NzGCAbk",  # picture
            "1neZGiBZjrnEJiWtDCbh0-u7UIus5P8WR",  # video
            "1NCEHcTwE1MSFpMmY35EVQjsjR1d7qZnZ",  # nsfw_video
            """photorealistic, high quality, skin detail, BREAK
            1girl, Asian, 18 years old, brown hair, medium-large breasts, slim waist, tan skin, thin lips, smirk, blue eyes""",
            [1, 0.7, 3, 1.4, -0.30, -1.5],
        ),
        setting2_generate_data(
            "ruthmonclaire",
            "1_jsV4GNTAa0PVmX8F4KlelAu4BFgL2kF",  # picture
            "1bro3C7Ialbj6ltMKvx804U3CU3kLMmj9",  # video
            "1A8irevxQpCLZ-IoOjH7d2kkAPrCGDQ9S",  # nsfw_video
            """photorealistic, high quality, skin detail, BREAK
            1girl, redhead, 18 years old, medium-large breasts, slim waist, tan skin, thin lips, smirk, blue eyes""",
            [1, 0.7, 2.25, 1.10, -1.70, -1.5],
        ),
        setting2_generate_data(
            "kenzienoir",
            "1o55kU-E9drxz2wLEiDgxWfrGHlaoulnr",  # picture
            "1eqHguRed-ANrWjUjDdxH2GXs_CBlreCO",  # video
            "1UOWiammfsu8kn_aFnfy9W9-SWU7KbBSD",  # nsfw_video
            "photorealistic portrait of an 18-year-old Asian girl with voluminous long ash-blonde hair, slim waist, medium saggy breasts, large hips, toned legs, tan skin, cute, big thin lips, smirk, bright blue eyes, sharp facial features and cheekbones, high quality and detail.",
            [1, 0.7, 1.6, 0.8, -0.75, -1.5, 1.1],
        ),
        setting2_generate_data(
            "janiceblair.xo",
            "1r_ccJ-zwLaDuWKlV8ymtO0QY4UcRGoR7",  # picture
            "1_UNb8ZqjhaDfk0-5zdvu54tTrnf243Yt",  # video
            "1VvHgESQrB5rex2ssiEKnbKbXvmJYq2BL",  # nsfw_video
            """photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, black hair, medium-large breasts, slim waist, tan skin, thin lips, smirk, blue eyes""",
            [1, 0.7, 0.90, 2.5, 0.50, -1.5],
        ),
        setting2_generate_data(
            "monikaroxley",
            "1zJ25DCsnB_4GL0_3m-VnprkAu44BP_Ip",  # picture
            "1bRjaIiDxiNm57kNpHF-5GXKCV9bRkCEY",  # video
            "1zx5pR5aWpr8aB53-7a5LLtPU_r0BBCDK",  # nsfw_video
            """photorealistic portrait of an 18-year-old sorority girl with voluminous long black hair, slim waist, medium saggy breasts, large hips, toned legs, tan skin, cute, big thin lips, smirk, bright blue eyes, sharp facial features and cheekbones, high quality and detail.""",
            [1, 0.7, 1.10, 1.85, 0.50, -1.5],
        ),
        setting2_generate_data(
            "kiaravouxelle",
            "1sBl52bL02xzjFPVa6MdG9C_5AZ_RoqAs",  # picture
            "1-I_3qVj0N7ToDu-1fjBAxqDV9fRHpXwl",  # video
            "1dm0-TeULgBb99RQgIiS0hjg7cFGqYWc3",  # nsfw_video
            """photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, ash-blonde hair, medium-large breasts, slim waist, tan skin, thin lips, smirk, blue eyes""",
            [1, 0.7, 1.95, 1.45, -1.15, -1.5, 1.1],
        ),
        setting2_generate_data(
            "lilith_rayne.xo",
            "14Sk-9RHb6NHFVapLqOZO_cfnvfn4fiJX",  # picture
            "1CX7jzPvTdwkJ6PeFsWXh17MPEb4Iakul",  # video
            "1zqKil1L8WThOn1Sb_yjqcU_7dgtvIzzr",  # nsfw_video
            """photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, ash-blonde hair, huge breasts, slim waist, tan skin, thin lips, smirk, blue eyes""",
            [1, 0.7, 2.20, 1.00, -2.30, -1.50],
        ),
        setting2_generate_data(
            "nicolevalaine",
            "1sZ3ea2uNlh7-kaJIVmsIRmfP5sF99tn8",  # picture
            "1RdFT0lBr10rKHDxaOLtRXtIb61l36Xiq",  # video
            "1nDN6TK65CSAO2mjtH1NzuzfaeKoYCMle",  # nsfw_video
            """photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, ash-blonde hair, huge breasts, slim waist, tan skin, thin lips, smirk, blue eyes""",
            [1, 0.7, 2.30, 1.20, -2.35, -1.50],
        ),
        setting2_generate_data(
            "kellymavrix",
            "1vY_89VRvgQpro-Ticyf1BxyCVdQPA7ka",  # picture
            "16x-4C5fdo2gALcd7wvu9hzS6U43ZBIuu",  # video
            "15y6Q1IuC8-ArUk0bnY8kEOHG_i8xzJaJ",  # nsfw_video
            """photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, ash-blonde hair, huge breasts, slim waist, tan skin, thin lips, smirk, blue eyes""",
            [1, 0.7, 3.45, 0.05, -1.70, -1.5],
        ),
        setting2_generate_data(
            "emilyzaylen",
            "1yPS-BlEZO_8bphZS2v3hQwkm8YvqKCLI",  # picture
            "17a1kB_XzCQNexYToW8mH2RdgsKVEVDEm",  # video
            "1CUP6gGFnwLw3HGHOul8tdItH6s5RBwoZ",  # nsfw_video
            """photorealistic, high quality, skin detail, BREAK
            1girl, Latina, 18 years old, brown hair, huge breasts, slim waist, tan skin, thin lips, smirk, blue eyes""",
            [1, 0.7, 1.10, 0.05, -1.70, -1.5],
        ),
        setting2_generate_data(
            "albabloomy",
            "1Dg7PcdufVeqX6Z4xO0oUra_8p9C5QQsw",  # picture
            "1XmGqJ56mab2Jt0Uidt53nVoaT55hd1Jj",  # video
            "13BJa1CqmGefEE5tg7cVrD8pKZT460Ro4",  # nsfw_video
            """photorealistic, high quality, skin detail, BREAK
            1girl, Latina, 18 years old, black hair, huge breasts, slim waist, tan skin, thin lips, smirk, blue eyes""",
            [1, 0.7, 3.80, 0.1, -3.00, -1.50],
        ),
    ]

    return dataArray