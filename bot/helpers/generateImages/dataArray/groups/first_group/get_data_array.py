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
            1girl, 18 years old, blonde hair, green eyes, tan skin, smiling.""",
            [2, 3.10, -0.90, -1.70, 1.50, 0.9, 1.00, 0.40],
        ),
        
        # setting_2 модели
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
            "nicolevalaine",
            47,
            "1sZ3ea2uNlh7-kaJIVmsIRmfP5sF99tn8",
            "1RdFT0lBr10rKHDxaOLtRXtIb61l36Xiq",
            "1nDN6TK65CSAO2mjtH1NzuzfaeKoYCMle",
            """photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, ash-blonde hair, huge breasts, slim waist, tan skin, thin lips, smirk, blue eyes""",
            [1, 0.7, 2.30, 1.20, -2.35, -1.50],
        ),
        setting2_generate_data(
            "albabloomy",
            50,
            "1Dg7PcdufVeqX6Z4xO0oUra_8p9C5QQsw",
            "1XmGqJ56mab2Jt0Uidt53nVoaT55hd1Jj",
            "13BJa1CqmGefEE5tg7cVrD8pKZT460Ro4",
            """photorealistic, high quality, skin detail, BREAK
            1girl, Latina, 18 years old, black hair, huge breasts, slim waist, tan skin, thin lips, smirk, blue eyes""",
            [1, 0.7, 3.80, 0.1, -3.00, -1.50],
        ),
        
        # setting_3 модели
        setting3_generate_data(
            "simona.caramella",
            62,
            "1HdkoJ7AbQCcTzK15rej69c_iaGYL99iP",
            "1gmxIHgpaSF-CvzbTgiqME-RFQh4qGwLg",
            "1Epg8G_mKJ0A7Xu_lN2w77MjVKgAQQ467",
            "photorealistic portrait, 18 years old, brown hair, big breasts, slim waist, tan skin, big lips, smirk, brown eyes, high quality.",
            [-1.50, 1.30, 0.7, 3.7, 0.10, -0.35],
        ),
        setting3_generate_data(
            "lolavexley",
            68,
            "1dUwCO9eBw7FVY15BoEDAFsPiV3y-aCWx",
            "1VLNdlBdq-eTJWYpJmrhfwnugIXYs1FQ9",
            "1q4KcwSblnbR4XPmZtC4WMGVow6w7L26O",
            """score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

            real_beauty, igbaddie, 1girl, 18 years old, sorority girl, volumnous brown hair, long hair, huge breasts, erect breasts, upright breasts, slim waist, big bubble butt, huge ass, hourglass body type, toned legs, tan skin, skinny, cute, big lips, thin lips, smirk, bright-blue eyes, sharp facial features, sharp cheekbones.""",
            [-1.50, 1.30, 0.7, 3.2, 1.95, -1.00],
        ),
        
        # setting_4 модели
        setting4_generate_data(
            "victoriadellor",
            78,
            "1hp5GLtfqhfoNYG6Ugn8tc7JF-uqSHLfJ",
            "1iQReqbA4XDnPW6pfYLq400u3IF6tgEG4",
            "1OLSVsw2cV75L4Nw7KgwB2LeYCiA47Oci",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK 
            1woman, milf, black hair, medium-large natural breasts, tan skin, green eyes""",
            [2, 4.30, -1.70, 1.00, 1.00, 1.70, -0.70, 0.35],
        ),
        setting4_generate_data(
            "rihannacorvelle",
            88,
            "13qV_K99ChXZhdnSKpBtbwvuNxV3Y49mO",
            "1iAyyzYFW0kgR-v5hF18aT4S6Ed8estRT",
            "1qcKmlJDkMKRdNxe_EB7gvxGo37xLrSAz",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK 
            1girl, 18, sorority girl, white-black hair, medium-large natural breasts, tan skin, blue eyes""",
            [2, 3.90, -2.50, 2.00, 1.52, 1.70, -0.70, 0.35],
        ),
        setting4_generate_data(
            "avacreston",
            93,
            "1OIPx2V6U6tj9AzL20nN0nAMlLFyV8wzh",
            "1zm1cI55s23ta4nLMO-avFZm2wgqeVr-D",
            "1yC0uiIAFfsxhYcokhs-jVaSSEvsZqnVv",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK 
            1girl, 18, sorority girl, black hair, medium-large natural breasts, extra tan skin, blue eyes""",
            [2, 2.1, -1.70, 3.2, 1.00, 1.70, -0.70, 0.35],
        ),
        setting4_generate_data(
            "jennifer_harrington.xo",
            97,
            "1mxmGqspHnlGaltzsJbdOeWek8K4U6ncz",
            "1BOA9b-TPtuFMlJ6Izi9TntHtvnX4NfYo",
            "1MKN5dp4IXt-OG2qP-vMrIsE0ZSkDGxLf",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK 
            1girl, 18, sorority girl, black hair, medium-large natural breasts, extra tan skin, blue eyes, smirk""",
            [2, 3.10, -1.70, 1.30, 1.00, 1.70, -0.70, 0.35, 0, 1.55],
        ),
    ]

    return data_array
