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
        # setting_2 модели
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
        setting2_generate_data(
            "carolinehazel.xo",
            51,
            "1Hdp3VL2CMzeob7qX5UVsbCn5he5-t6az",
            "1lxWDRkM5oA6_ugRHvQFUntysIUd9KGQy",
            "1lTb92NPF7sHOsYmRaDVflv7N2r1IVj3d",
            "photorealistic portrait, 18 years old, ash-blonde hair, big breasts, slim waist, tan skin, smirk, high quality.",
            [-1.50, 1.30, 0.7, 3.20, 0.45, -1.00],
        ),
        
        # setting_3 модели
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
            "simona.caramella",
            62,
            "1HdkoJ7AbQCcTzK15rej69c_iaGYL99iP",
            "1gmxIHgpaSF-CvzbTgiqME-RFQh4qGwLg",
            "1Epg8G_mKJ0A7Xu_lN2w77MjVKgAQQ467",
            "photorealistic portrait, 18 years old, brown hair, big breasts, slim waist, tan skin, big lips, smirk, brown eyes, high quality.",
            [-1.50, 1.30, 0.7, 3.7, 0.10, -0.35],
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
            "ashleymoreaux.xo",
            96,
            "1jiLVZCzXLu8m4ZECwciGbZz6jhWVbBQ8",
            "1QzRyaI7FboYtdDDtycf19FX9G_7atYQN",
            "1VOSRqtGLELBE7sSxQJLKt4JD0W2Hqb4K",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK 
            1girl, 18, sorority girl, black hair, medium-large natural breasts, extra tan skin, blue eyes, smirk""",
            [2, 2.70, -1.70, 1.95, 1.00, 1.70, -0.70, 0.35, 0, 1.25],
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
        setting4_generate_data(
            "jessie_valemont",
            98,
            "1mxmGqspHnlGaltzsJbdOeWek8K4U6ncz",
            "1BOA9b-TPtuFMlJ6Izi9TntHtvnX4NfYo",
            "1MKN5dp4IXt-OG2qP-vMrIsE0ZSkDGxLf",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK 
            1girl, 18, sorority girl, black hair, medium-large natural breasts, extra tan skin, blue eyes, smirk""",
            [2, 3.10, -1.70, 1.30, 1.00, 1.70, -0.70, 0.35, 0, 1.55],
        ),
    ]

    return data_array
