from bot.helpers.generateImages.dataArray.settings.setting_1.generate_data import (
    setting1_generate_data,
)
from bot.helpers.generateImages.dataArray.settings.setting_2.generate_data import (
    setting2_generate_data,
)


def first_group_get_data_array():
    # Массив дат с нужными параметрами для запроса
    data_array = [
        # setting_1 модели
        setting1_generate_data(
            model_name="chloemay.xo.xo",
            model_index=3,
            picture_folder_id="1k5VoyK5pOmVLzzONNadgWGiJrXWjuUXG",
            video_folder_id="1BXpNVoneM0nSISQzyxsO9mG5SqzztP0t",
            nsfw_video_folder_id="1As1OBjTIhckVo1APY0oiM_Db1HwbBhXO",
            prompt="""photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 20 years old, athletic body, brown hair, blue eyes, natural skin texture.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            loras_weights=[2, 2.9, -0.9, -1.7, 1.8, 0.9, 1, 0.8],
        ),
        setting1_generate_data(
            model_name="brittany_cross.xo",
            model_index=6,
            picture_folder_id="10sDc9ypgszlwXRmD6_V_FHz_f9CIK6Rx",
            video_folder_id="1_20xxewMNIaO31v06yvUwn-1bKUHaNFI",
            nsfw_video_folder_id="1UGGBVhIgTx-JooGysreAQ4MV7PPZMBor",
            prompt="""photorealistic, high quality, vibrant colors, bright lighting, skin detail, BREAK
            1girl, 18 years old, athletic, blonde hair, brown eyes, fair skin, slight smile.
            Style: realistic photo, Canon DSLR, soft daylight.""",
            loras_weights=[2, 3.10, -0.90, -1.10, 1.75, 0.6, 0.65, 0.80],
        ),
        setting1_generate_data(
            model_name="sierravexley",
            model_index=10,
            picture_folder_id="12bi_ufYXj71QzV1jTHTSjYmAjPr2Utky",
            video_folder_id="1Hcw9aO89wyw4dco86kt5RRCC-Ue8Rebo",
            nsfw_video_folder_id="1SNri9MEsRnJz9NF3YdJdub6h2X0efssM",
            prompt="""photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, brown hair, blue eyes, tanned skin, ponytail.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            loras_weights=[2, 1.60, -0.90, -1.70, 2.80, 1.00, 2.65, 0.80],
        ),
        setting1_generate_data(
            model_name="naomiruelle",
            model_index=23,
            picture_folder_id="1ye6AlCgZG_TkvRwCXxArM2rDI1x6kF20",
            video_folder_id="1-suMtU3kX2zFR12Pchm05pmvnYQdrxYy",
            nsfw_video_folder_id="1Bp5fPqB-rgvZe_SDblTCsetIfS-7y_HJ",
            prompt="""photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic, blonde hair, green eyes, tanned skin.
            Style: Instagram photo style, Canon DSLR, bright sunlight""",
            loras_weights=[2, 0.65, -0.90, -1.70, 3.7, 1.25, 1.75, 1.00],
        ),
        setting1_generate_data(
            model_name="miahazelton.xo",
            model_index=24,
            picture_folder_id="1uvYUlkG_A902uAmYwNWlXcqbYRo4hA07",
            video_folder_id="1LCR_JQEg2JIisADrnochKASReWbUCfrb",
            nsfw_video_folder_id="18dssne4ftnQl6bwpY9QYj01UIp69HFbp",
            prompt="""photorealistic, high quality, BREAK
            1girl, 18 years old, blonde hair, green eyes, medium tan skin, smiling.""",
            loras_weights=[2, 3.10, -0.90, -1.70, 1.50, 0.9, 1.00, 0.40],
        ),
        setting1_generate_data(
            model_name="sasharoxelle",
            model_index=25,
            picture_folder_id="1CC3xxDdpYqmDH-4Bm-HVA32EghXdgZlK",
            video_folder_id="1scBkcxWIWasoo84FTO2M_VVb_4bnqIYX",
            nsfw_video_folder_id="14Q0ENXHYlVVV7Xm173D6C9oNQ_4O6jo5",
            prompt="""photorealistic, high quality, BREAK
            1girl, 18 years old, brown hair, blue eyes, tan skin, smiling.""",
            loras_weights=[2, 1.00, -0.90, -0.35, 2.5, 1.00, 1.60, 0.55, 1.95],
        ),
        # setting_2 модели
        setting2_generate_data(
            model_name="vanessadior.xo",
            model_index=26,
            picture_folder_id="1YpXc8m9btjYfoHD0fDbji0FpFrpruBSg",
            video_folder_id="17u0_0ZiKmMDO3kn7m-SKPFoWBOH59v2I",
            nsfw_video_folder_id="16rm09bVW2eBM_3_JNne1K6wkIxku-LJp",
            prompt="""photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, ash-blonde hair, huge breasts, slim waist, tan skin, plump lips, smirk, blue eyes""",
            loras_weights=[1, 0.7, 2.5, 1, -1.05, -1.5],
        ),
        setting2_generate_data(
            model_name="celinemyrren",
            model_index=28,
            picture_folder_id="15gfR1qOglE1kWWu5oc1XpbzoHkj4idXi",
            video_folder_id="1BlPotHzWPwiEzE9BKQPh8vSy4vzWVVB0",
            nsfw_video_folder_id="1vOfFUGtvfMXWAKH_f_nHIo3WdBwh1M3h",
            prompt="""photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, brown hair, huge breasts, slim waist, tan skin, plump lips, smirk, green eyes""",
            loras_weights=[1, 0.7, 1.9, 0, -0.15, -1.5],
        ),
        setting2_generate_data(
            model_name="gracelowell.xo",
            model_index=29,
            picture_folder_id="1O0oMnQj5bFzNPhJGpzwHuWIDPxlX2UJ8",
            video_folder_id="1T9ptTmprKmueWa9G6MKZf4x56bXQiEf0",
            nsfw_video_folder_id="1qEiJD2I1THle_JUAIClz41eZAVht4iMs",
            prompt="""photorealistic portrait of an 18-year-old sorority girl with voluminous long blonde hair, slim waist, huge breasts, large hips, toned legs, tan skin, cute, big thin lips, smirk, bright green eyes, high quality and detail.""",
            loras_weights=[1, 0.7, 1.9, 0.05, -0.85, -1.5],
        ),
        setting2_generate_data(
            model_name="valeriagomez.xo",
            model_index=30,
            picture_folder_id="1SfIAd7S_W8RGHBatjWx3NXPpWsskZaGS",
            video_folder_id="18BQ8yxwk9PhZbeQMUNo2-xQjb-kO_La8",
            nsfw_video_folder_id="1m1TxycO1m2eYADqUIv7LILlvXa33JVe7",
            prompt="""photorealistic portrait of an 18-year-old Arabian girl with voluminous long black hair, slim waist, large breasts and hips, toned legs, high tan skin, big plump lips, smirk, bright brown eyes, realistic style, high quality and detail.""",
            loras_weights=[1, 0.7, 3, 0.6, -0.35, -1.5],
        ),
        setting2_generate_data(
            model_name="ivyxhart",
            model_index=31,
            picture_folder_id="1SfIAd7S_W8RGHBatjWx3NXPpWsskZaGS",
            video_folder_id="18BQ8yxwk9PhZbeQMUNo2-xQjb-kO_La8",
            nsfw_video_folder_id="1m1TxycO1m2eYADqUIv7LILlvXa33JVe7",
            prompt="""photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, black hair, huge breasts, slim waist, tan skin, plump lips, smirk, blue eyes""",
            loras_weights=[1, 0.7, 2.5, 1, -1.05, -1.5],
        ),
        setting2_generate_data(
            model_name="ellamaddix.xo",
            model_index=32,
            picture_folder_id="1SfIAd7S_W8RGHBatjWx3NXPpWsskZaGS",
            video_folder_id="18BQ8yxwk9PhZbeQMUNo2-xQjb-kO_La8",
            nsfw_video_folder_id="1m1TxycO1m2eYADqUIv7LILlvXa33JVe7",
            prompt="""photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, ash-blonde hair, huge breasts, slim waist, tan skin, plump lips, smirk, blue eyes""",
            loras_weights=[1, 0.7, 2.5, 1, -1.05, -1.5],
        ),
        setting2_generate_data(
            model_name="mileyleclair.xo",
            model_index=33,
            picture_folder_id="1MLHRGi12Xt_QZ7qM5YFoS-Y_JiYU1YZs",
            video_folder_id="10Tcl469LW5fCwTjqhKMLNROB9YgIY6ON",
            nsfw_video_folder_id="1nIU2pOpoDf3rE0T1zgxO3vcIroU2RL10",
            prompt="""photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, blonde hair, huge breasts, slim waist, tan skin, thin lips, smirk, green eyes""",
            loras_weights=[1, 0.7, 2.00, 1.20, -2.70, -1.50],
        ),
        setting2_generate_data(
            model_name="thea_azelle",
            model_index=34,
            picture_folder_id="1SfIAd7S_W8RGHBatjWx3NXPpWsskZaGS",
            video_folder_id="18BQ8yxwk9PhZbeQMUNo2-xQjb-kO_La8",
            nsfw_video_folder_id="1m1TxycO1m2eYADqUIv7LILlvXa33JVe7",
            prompt="""photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, ash-blonde hair, huge breasts, slim waist, tan skin, plump lips, smirk, blue eyes""",
            loras_weights=[1, 0.7, 2.5, 1, -1.05, -1.5],
        ),
        setting2_generate_data(
            model_name="briaclaire.xo",
            model_index=35,
            picture_folder_id="1SfIAd7S_W8RGHBatjWx3NXPpWsskZaGS",
            video_folder_id="18BQ8yxwk9PhZbeQMUNo2-xQjb-kO_La8",
            nsfw_video_folder_id="1m1TxycO1m2eYADqUIv7LILlvXa33JVe7",
            prompt="""photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, black hair, huge breasts, slim waist, tan skin, plump lips, smirk, blue eyes""",
            loras_weights=[1, 0.7, 2.5, 1, -1.05, -1.5],
        ),
        setting2_generate_data(
            model_name="rinazuri",
            model_index=36,
            picture_folder_id="1SfIAd7S_W8RGHBatjWx3NXPpWsskZaGS",
            video_folder_id="18BQ8yxwk9PhZbeQMUNo2-xQjb-kO_La8",
            nsfw_video_folder_id="1m1TxycO1m2eYADqUIv7LILlvXa33JVe7",
            prompt="""photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, ash-blonde hair, huge breasts, slim waist, tan skin, plump lips, smirk, blue eyes""",
            loras_weights=[1, 0.7, 2.5, 1, -1.05, -1.5],
        ),
        setting2_generate_data(
            model_name="mari_avellin",
            model_index=37,
            picture_folder_id="1YpXc8m9btjYfoHD0fDbji0FpFrpruBSg",
            video_folder_id="17u0_0ZiKmMDO3kn7m-SKPFoWBOH59v2I",
            nsfw_video_folder_id="16rm09bVW2eBM_3_JNne1K6wkIxku-LJp",
            prompt="""photorealistic, high quality, skin detail, BREAK
            1girl, 30 years old, ash-blonde hair, huge breasts, slim waist, tan skin, plump lips, smirk, brown eyes""",
            loras_weights=[1, 0.7, 1.00, -0.10, -0.60, -1.50],
        ),
        setting2_generate_data(
            model_name="amirawellex",
            model_index=38,
            picture_folder_id="1YpXc8m9btjYfoHD0fDbji0FpFrpruBSg",
            video_folder_id="17u0_0ZiKmMDO3kn7m-SKPFoWBOH59v2I",
            nsfw_video_folder_id="16rm09bVW2eBM_3_JNne1K6wkIxku-LJp",
            prompt="""photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, black hair, huge breasts, slim waist, tan skin, plump lips, smirk, blue eyes""",
            loras_weights=[1, 0.7, 2.5, 1, -1.05, -1.5],
        ),
        setting2_generate_data(
            model_name="dianadelmar.xo",
            model_index=39,
            picture_folder_id="1YpXc8m9btjYfoHD0fDbji0FpFrpruBSg",
            video_folder_id="17u0_0ZiKmMDO3kn7m-SKPFoWBOH59v2I",
            nsfw_video_folder_id="16rm09bVW2eBM_3_JNne1K6wkIxku-LJp",
            prompt="""photorealistic, high quality, skin detail, BREAK
            1girl, Asian, 18 years old, brown hair, medium-large breasts, slim waist, tan skin, thin lips, smirk, blue eyes""",
            loras_weights=[1, 0.7, 3.70, 1.35, -2.40, -1.50],
        ),
        setting2_generate_data(
            model_name="kaiastell",
            model_index=40,
            picture_folder_id="1YpXc8m9btjYfoHD0fDbji0FpFrpruBSg",
            video_folder_id="17u0_0ZiKmMDO3kn7m-SKPFoWBOH59v2I",
            nsfw_video_folder_id="16rm09bVW2eBM_3_JNne1K6wkIxku-LJp",
            prompt="""photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, black hair, huge breasts, slim waist, tan skin, plump lips, smirk, blue eyes""",
            loras_weights=[1, 0.7, 2.5, 1, -1.05, -1.5],
        ),
        setting2_generate_data(
            model_name="ruthmonclaire",
            model_index=41,
            picture_folder_id="1YpXc8m9btjYfoHD0fDbji0FpFrpruBSg",
            video_folder_id="17u0_0ZiKmMDO3kn7m-SKPFoWBOH59v2I",
            nsfw_video_folder_id="16rm09bVW2eBM_3_JNne1K6wkIxku-LJp",
            prompt="""photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, red hair, huge breasts, slim waist, tan skin, plump lips, smirk, blue eyes""",
            loras_weights=[1, 0.7, 2.5, 1, -1.05, -1.5],
        ),
        setting2_generate_data(
            model_name="kenzienoir",
            model_index=42,
            picture_folder_id="1YpXc8m9btjYfoHD0fDbji0FpFrpruBSg",
            video_folder_id="17u0_0ZiKmMDO3kn7m-SKPFoWBOH59v2I",
            nsfw_video_folder_id="16rm09bVW2eBM_3_JNne1K6wkIxku-LJp",
            prompt="""photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, ash-blonde hair, huge breasts, slim waist, tan skin, plump lips, smirk, blue eyes""",
            loras_weights=[1, 0.7, 2.5, 1, -1.05, -1.5],
        ),
        setting2_generate_data(
            model_name="janiceblair.xo",
            model_index=43,
            picture_folder_id="1YpXc8m9btjYfoHD0fDbji0FpFrpruBSg",
            video_folder_id="17u0_0ZiKmMDO3kn7m-SKPFoWBOH59v2I",
            nsfw_video_folder_id="16rm09bVW2eBM_3_JNne1K6wkIxku-LJp",
            prompt="""photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, black hair, huge breasts, slim waist, tan skin, plump lips, smirk, blue eyes""",
            loras_weights=[1, 0.7, 2.5, 1, -1.05, -1.5],
        ),
        setting2_generate_data(
            model_name="monikaroxley",
            model_index=44,
            picture_folder_id="1YpXc8m9btjYfoHD0fDbji0FpFrpruBSg",
            video_folder_id="17u0_0ZiKmMDO3kn7m-SKPFoWBOH59v2I",
            nsfw_video_folder_id="16rm09bVW2eBM_3_JNne1K6wkIxku-LJp",
            prompt="""photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, black hair, huge breasts, slim waist, tan skin, plump lips, smirk, blue eyes""",
            loras_weights=[1, 0.7, 2.5, 1, -1.05, -1.5],
        ),
        setting2_generate_data(
            model_name="kiaravouxelle",
            model_index=45,
            picture_folder_id="1YpXc8m9btjYfoHD0fDbji0FpFrpruBSg",
            video_folder_id="17u0_0ZiKmMDO3kn7m-SKPFoWBOH59v2I",
            nsfw_video_folder_id="16rm09bVW2eBM_3_JNne1K6wkIxku-LJp",
            prompt="""photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, ash-blonde hair, huge breasts, slim waist, tan skin, plump lips, smirk, blue eyes""",
            loras_weights=[1, 0.7, 2.5, 1, -1.05, -1.5],
        ),
        setting2_generate_data(
            model_name="lilith_rayne",
            model_index=46,
            picture_folder_id="1YpXc8m9btjYfoHD0fDbji0FpFrpruBSg",
            video_folder_id="17u0_0ZiKmMDO3kn7m-SKPFoWBOH59v2I",
            nsfw_video_folder_id="16rm09bVW2eBM_3_JNne1K6wkIxku-LJp",
            prompt="""photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, ash-blonde hair, huge breasts, slim waist, tan skin, plump lips, smirk, blue eyes""",
            loras_weights=[1, 0.7, 2.5, 1, -1.05, -1.5],
        ),
        setting2_generate_data(
            model_name="nicolevalaine",
            model_index=47,
            picture_folder_id="1YpXc8m9btjYfoHD0fDbji0FpFrpruBSg",
            video_folder_id="17u0_0ZiKmMDO3kn7m-SKPFoWBOH59v2I",
            nsfw_video_folder_id="16rm09bVW2eBM_3_JNne1K6wkIxku-LJp",
            prompt="""photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, ash-blonde hair, huge breasts, slim waist, tan skin, plump lips, smirk, blue eyes""",
            loras_weights=[1, 0.7, 2.5, 1, -1.05, -1.5],
        ),
        setting2_generate_data(
            model_name="kellymavrix",
            model_index=48,
            picture_folder_id="1YpXc8m9btjYfoHD0fDbji0FpFrpruBSg",
            video_folder_id="17u0_0ZiKmMDO3kn7m-SKPFoWBOH59v2I",
            nsfw_video_folder_id="16rm09bVW2eBM_3_JNne1K6wkIxku-LJp",
            prompt="""photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, ash-blonde hair, huge breasts, slim waist, tan skin, plump lips, smirk, blue eyes""",
            loras_weights=[1, 0.7, 2.5, 1, -1.05, -1.5],
        ),
        setting2_generate_data(
            model_name="emilyzaylen",
            model_index=49,
            picture_folder_id="1YpXc8m9btjYfoHD0fDbji0FpFrpruBSg",
            video_folder_id="17u0_0ZiKmMDO3kn7m-SKPFoWBOH59v2I",
            nsfw_video_folder_id="16rm09bVW2eBM_3_JNne1K6wkIxku-LJp",
            prompt="""photorealistic, high quality, skin detail, BREAK
            1girl, 18 years old, black hair, huge breasts, slim waist, tan skin, plump lips, smirk, blue eyes""",
            loras_weights=[1, 0.7, 2.5, 1, -1.05, -1.5],
        ),
    ]

    return data_array
