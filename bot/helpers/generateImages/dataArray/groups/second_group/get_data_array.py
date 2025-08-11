# Функция для генерации массива данных для запроса для второй группы
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
            model_name="albabloomy",
            model_index=50,
            picture_folder_id="1Dg7PcdufVeqX6Z4xO0oUra_8p9C5QQsw",
            video_folder_id="1XmGqJ56mab2Jt0Uidt53nVoaT55hd1Jj",
            nsfw_video_folder_id="13BJa1CqmGefEE5tg7cVrD8pKZT460Ro4",
            prompt="""photorealistic, high quality, skin detail, BREAK
            1girl, Latina, 18 years old, black hair, huge breasts, slim waist, tan skin, thin lips, smirk, blue eyes""",
            loras_weights=[1, 0.7, 3.60, 0, -3.00, -1.50],
        ),
        # setting_3 модели
        setting3_generate_data(
            model_name="carolinehazel.xo",
            model_index=51,
            picture_folder_id="1Hdp3VL2CMzeob7qX5UVsbCn5he5-t6az",
            video_folder_id="1lxWDRkM5oA6_ugRHvQFUntysIUd9KGQy",
            nsfw_video_folder_id="1lTb92NPF7sHOsYmRaDVflv7N2r1IVj3d",
            prompt="""score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

            real_beauty, igbaddie, 1girl, 18 years old, sorority girl, volumnous ash-blonde hair, long hair, huge breasts, erect breasts, upright breasts, slim waist, big bubble butt, huge ass, hourglass body type, toned legs, tan skin, skinny, cute, big lips, thin lips, smirk, bright-blue eyes, sharp facial features, sharp cheekbones.""",
            loras_weights=[-1.50, 1.30, 1.3, 3, 0.25, -1.70],
        ),
        setting3_generate_data(
            model_name="dasharomanova.xo",
            model_index=59,
            picture_folder_id="1yalGaEVfgs9QOWHd93qfRejhnnM8Z07L",
            video_folder_id="19YGecBXjT0-Zs9lWgw_AV7DFTp9phAFG",
            nsfw_video_folder_id="1movOYETVPHNZkrzadfva4REhsVJ5-mkt",
            prompt="photorealistic portrait, 18 years old, platinum-blonde hair with black curls, huge breasts, slim waist, big bubble butt, tan skin, big lips, smirk, green eyes, high quality.",
            loras_weights=[-1.50, 1.30, 0.75, 3, 1.60, -0.85],
        ),
        setting3_generate_data(
            model_name="zlatapavlova.xo",
            model_index=61,
            picture_folder_id="1yfDlRMdThAacSl0WZ-DQZxxDRYFGeEqY",
            video_folder_id="1KY5NttoHI1ZvaRLjqsNfMp33AjhyuxM-",
            nsfw_video_folder_id="1WadINZaETk_qE2fIeYG6Lm3iEa6VbxU6",
            prompt="photorealistic portrait, 18 years old, platinum-blonde hair with black curls, huge breasts, slim waist, big bubble butt, tan skin, big lips, smirk, green eyes, high quality.",
            loras_weights=[-1.50, 1.30, 0.7, 2.40, 1.5, -1.00],
        ),
        setting3_generate_data(
            model_name="simona.caramella",
            model_index=62,
            picture_folder_id="1HdkoJ7AbQCcTzK15rej69c_iaGYL99iP",
            video_folder_id="1gmxIHgpaSF-CvzbTgiqME-RFQh4qGwLg",
            nsfw_video_folder_id="1Epg8G_mKJ0A7Xu_lN2w77MjVKgAQQ467",
            prompt="photorealistic portrait, 18 years old, brown hair, big breasts, slim waist, tan skin, big lips, smirk, brown eyes, high quality.",
            loras_weights=[-1.50, 1.30, 0.7, 3.7, 0.10, -0.35],
        ),
        setting3_generate_data(
            model_name="callieroux",
            model_index=66,
            picture_folder_id="1aWuuB7pRutNzGIKGrLuUsep7McH3OxYd",
            video_folder_id="1mRwEJ7Y64hQXWBkMODZ1LZgSOQ_vg66p",
            nsfw_video_folder_id="1_p8Bh8Ad11uEXldIhqEcuqVSoFTVVH6N",
            prompt="photorealistic portrait, 18 years old, ash-blonde hair, big breasts, slim waist, tan skin, smirk, high quality.",
            loras_weights=[-1.50, 1.30, 0.7, 3.65, -0.20, 0.30],
        ),
        setting3_generate_data(
            model_name="lolavexley",
            model_index=68,
            picture_folder_id="1dUwCO9eBw7FVY15BoEDAFsPiV3y-aCWx",
            video_folder_id="1VLNdlBdq-eTJWYpJmrhfwnugIXYs1FQ9",
            nsfw_video_folder_id="1q4KcwSblnbR4XPmZtC4WMGVow6w7L26O",
            prompt="""score_9, score_8_up, score_7_up, source_photo, source_real, hyper-realistic, photorealism, high detailed, high quality, masterpiece, photography, photorealistic, 8k detail, detailed background, ultra-detailed, vibrant colors, bright lighting, skin detail, BREAK

            real_beauty, igbaddie, 1girl, 18 years old, sorority girl, volumnous brown hair, long hair, huge breasts, erect breasts, upright breasts, slim waist, big bubble butt, huge ass, hourglass body type, toned legs, tan skin, skinny, cute, big lips, thin lips, smirk, bright-blue eyes, sharp facial features, sharp cheekbones.""",
            loras_weights=[-1.50, 1.30, 0.7, 3.2, 1.95, -1.00],
        ),
        
        # setting_4 модели
        setting4_generate_data(
            model_name="victoriadellor",
            model_index=78,
            picture_folder_id="1hp5GLtfqhfoNYG6Ugn8tc7JF-uqSHLfJ",
            video_folder_id="1iQReqbA4XDnPW6pfYLq400u3IF6tgEG4",
            nsfw_video_folder_id="1OLSVsw2cV75L4Nw7KgwB2LeYCiA47Oci",
            prompt="""photorealistic, high quality, vibrant colors, skin detail, BREAK 
            1woman, milf, black hair, medium-large natural breasts, tan skin, green eyes""",
            loras_weights=[2, 4.30, -1.70, 1.00, 1.00, 1.70, -0.70, 0.35],
        ),
        setting4_generate_data(
            model_name="evelynlaine.xo.xo",
            model_index=79,
            picture_folder_id="1RRN7ED5wdYaKaCNJlGMqAAqUgjAFmkh6",
            video_folder_id="1ZQoPo0PmGYdqAPzmsaM_PO1WIdsCSzRh",
            nsfw_video_folder_id="10dyGFZHQ22QM-Z3dNhSB_KEdJvVH5aSB",
            prompt="""photorealistic, high quality, vibrant colors, skin detail, BREAK 
            1girl, 18, sorority girl, platinum-blonde hair, medium-large natural breasts, tan skin, green eyes""",
            loras_weights=[2, 3.00, -2.00, 1.80, 2.00, 1.70, -0.70, 0.75],
        ),
        setting4_generate_data(
            model_name="abrilberries",
            model_index=82,
            picture_folder_id="1aE9PT_0HGK6At3iNefEsfYyAyYIBoQdQ",
            video_folder_id="1Pv7mPHnhts33aikK43OhzVntB8kURiDC",
            nsfw_video_folder_id="11B6AWrBo22EtY-Vd3kpmfP17WWewmTtf",
            prompt="""photorealistic, high quality, vibrant colors, skin detail, BREAK 
            1girl, 18, sorority girl, black hair, short hair, medium-large natural breasts, tan skin, green eyes""",
            loras_weights=[2, 1.90, -1.70, 3.90, 1.00, 1.70, -0.70, 0.35],
        ),
        setting4_generate_data(
            model_name="carmenkiss.xo",
            model_index=83,
            picture_folder_id="1pVXZOO4g0tnGssdZDEZBvVAdDCreI7Or",
            video_folder_id="1wkNrb70731x45zvo7FwKscEJYCYk0-0E",
            nsfw_video_folder_id="1k4wWqWfPwde9GdHZ8rECiQxhEIxYARCL",
            prompt="""photorealistic, high quality, vibrant colors, skin detail, BREAK 
            1girl, 18, sorority girl, black hair, medium-large natural breasts, tan skin, green eyes""",
            loras_weights=[2, 1.50, -0.10, 1.70, 1.00, 1.70, -0.70, 0.35],
        ),
        setting4_generate_data(
            model_name="marinalolita.xo",
            model_index=86,
            picture_folder_id="1hchSQ3dpHU5ugYithqcO_HTqjVri0yLz",
            video_folder_id="1JthmZV1fIMvXxVCEl9HaS23Yegh0TBYK",
            nsfw_video_folder_id="1rdOu2u2hOcqtP74kNWmb5fsYgWaLEqxO",
            prompt="""photorealistic, high quality, vibrant colors, skin detail, BREAK 
            1girl, 18, sorority girl, black hair, medium-large natural breasts, tan skin, green eyes""",
            loras_weights=[2, 1.90, -0.1, 0.85, 2.00, 1.70, -0.70, 0.35],
        ),
        setting4_generate_data(
            model_name="rihannacorvelle",
            model_index=88,
            picture_folder_id="13qV_K99ChXZhdnSKpBtbwvuNxV3Y49mO",
            video_folder_id="1iAyyzYFW0kgR-v5hF18aT4S6Ed8estRT",
            nsfw_video_folder_id="1qcKmlJDkMKRdNxe_EB7gvxGo37xLrSAz",
            prompt="""photorealistic, high quality, vibrant colors, skin detail, BREAK 
            1girl, 18, sorority girl, white-black hair, medium-large natural breasts, tan skin, blue eyes""",
            loras_weights=[2, 3.90, -2.50, 2.00, 1.52, 1.70, -0.70, 0.35],
        ),
        setting4_generate_data(
            model_name="beatricemeltie",
            model_index=89,
            picture_folder_id="1G4Zm21FBH-MYAE6IdyaLaChalkQAj-Od",
            video_folder_id="1BR5Z-y5WyYg3E-MeQt8UwF6VVYAAOug0",
            nsfw_video_folder_id="1ASjnAtaa8DaTp9YXCX_2NWYV-DhCuB4B",
            prompt="""photorealistic, high quality, vibrant colors, skin detail, BREAK 
            1girl, 18, sorority girl, white-black hair, medium-large natural breasts, tan skin, blue eyes""",
            loras_weights=[2, 0.70, -0.80, 3.05, 1.00, 1.70, -0.70, 0.35],
        ),
        setting4_generate_data(
            model_name="avacreston",
            model_index=93,
            picture_folder_id="1OIPx2V6U6tj9AzL20nN0nAMlLFyV8wzh",
            video_folder_id="1zm1cI55s23ta4nLMO-avFZm2wgqeVr-D",
            nsfw_video_folder_id="1yC0uiIAFfsxhYcokhs-jVaSSEvsZqnVv",
            prompt="""photorealistic, high quality, vibrant colors, skin detail, BREAK 
            1girl, 18, sorority girl, black hair, medium-large natural breasts, extra tan skin, blue eyes""",
            loras_weights=[2, 2.1, -1.70, 3.2, 1.00, 1.70, -0.70, 0.35],
        ),
        setting4_generate_data(
            model_name="ashleymoreaux.xo",
            model_index=96,
            picture_folder_id="1jiLVZCzXLu8m4ZECwciGbZz6jhWVbBQ8",
            video_folder_id="1QzRyaI7FboYtdDDtycf19FX9G_7atYQN",
            nsfw_video_folder_id="1VOSRqtGLELBE7sSxQJLKt4JD0W2Hqb4K",
            prompt="""photorealistic, high quality, vibrant colors, skin detail, BREAK 
            1girl, 18, sorority girl, black hair, medium-large natural breasts, extra tan skin, blue eyes, smirk""",
            loras_weights=[2, 2.70, -1.70, 1.95, 1.00, 1.70, -0.70, 0.35, 0, 1.25],
        ),
        setting4_generate_data(
            model_name="jennifer_harrington.xo",
            model_index=97,
            picture_folder_id="1mxmGqspHnlGaltzsJbdOeWek8K4U6ncz",
            video_folder_id="1BOA9b-TPtuFMlJ6Izi9TntHtvnX4NfYo",
            nsfw_video_folder_id="1MKN5dp4IXt-OG2qP-vMrIsE0ZSkDGxLf",
            prompt="""photorealistic, high quality, vibrant colors, skin detail, BREAK 
            1girl, 18, sorority girl, black hair, medium-large natural breasts, extra tan skin, blue eyes, smirk""",
            loras_weights=[2, 3.10, -1.70, 1.30, 1.00, 1.70, -0.70, 0.35, 0, 1.55],
        ),
        setting4_generate_data(
            model_name="jessie_valemont",
            model_index=98,
            picture_folder_id="1gu_1ckP6nfPFQaNKbDJXXotcDHFf4UWl",
            video_folder_id="1AKsI6PDvox_vE_R6FK63fO08Xi93j4mT",
            nsfw_video_folder_id="1BzkfzG1JviFkK714lD5OdOrVsgMExyJA",
            prompt="""photorealistic, high quality, vibrant colors, skin detail, BREAK 
            1girl, 18, sorority girl, white hair, medium-large natural breasts, extra tan skin, blue eyes, smirk""",
            loras_weights=[2, 3.10, -1.70, 1.30, 1.00, 1.70, -0.70, 0.35, 0, 1.55],
        ),
    ]

    return data_array
