from bot.helpers.generateImages.dataArray.setting_1.generate_data import (
    setting1_generate_data,
)
from bot.settings import settings


# Функция для генерации массива данных для запроса для настройки 1
def setting1_get_data_array():
    # Массив дат с нужными параметрами для запроса
    dataArray = [
        setting1_generate_data(
            "evanoir.xo",
            "1bto4oidFfiRif1UYk7jV5Smy8XhGaqDd",  # picture
            "10ZrWK48ExpqAR-OsDu8RBPYv-n61f0Ee",  # video
            "1ckx4EfT0G0N8jFyVgPRXJhehlc117Eni",  # nsfw_video
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 20 years old, athletic body, brown hair, blue eyes, natural skin texture.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            [2, 2.2, -0.9, -1.5, 1.5, 1.0, 1.85, 1.0, 0.35],
        ),
        setting1_generate_data(
            "nika_saintclair",
            "1wcHTTKyceJ8hADZU54tHyZCon08feiN_",
            "1GFTxvmKj6lA4U-SG40FqA0tp8MZPndSX",
            "14NBF4xN3eDb4idXbZnio9aG7JTWfL2gk",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 20 years old, athletic body, brown hair, blue eyes, natural skin texture.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            [2, 2.6, -0.9, -1.5, 1.4, 1.0, 1.40, 1.0],
        ),
        setting1_generate_data(
            "chloemay",
            "1k5VoyK5pOmVLzzONNadgWGiJrXWjuUXG",
            "1BXpNVoneM0nSISQzyxsO9mG5SqzztP0t",
            "1As1OBjTIhckVo1APY0oiM_Db1HwbBhXO",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 20 years old, athletic body, brown hair, blue eyes, natural skin texture.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            [2, 2.9, -0.9, -1.7, 1.8, 0.9, 1, 0.8],
        ),
        setting1_generate_data(
            "arialennix",
            "1EARI_gLremFbwGh9SizSc2UEVKBcT2rc",
            "1Efqfyr4VWMnpQd68I9lezVc3MrA6571n",
            "1Sx8iNeY4jOabkqxPkxvAjSaPx7vaADmI",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 20 years old, skinny body, black hair, brown eyes, natural skin texture.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            [2, 1.80, -0.90, -1.70, 1.60, 1.00, 1.00, 0.80],
        ),
        setting1_generate_data(
            "miaroxelle",
            "1pS6bQ1kMlqepc04gY2G4XA2-nKO3xpZu",
            "1ThGywKzpA9Qdg9mnuhk7CEc0Fla61EWx",
            "19uJHR1sGnLHBOfII88WaYEs0bwXU8wJ5",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, asian, 18 years old, athletic body, blonde hair, brown eyes, white skin.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            [2, 3.10, -0.90, -1.10, 0.9, 1.00, 1.00, 0.80],
        ),
        setting1_generate_data(
            "brittany_cross.xo",
            "10sDc9ypgszlwXRmD6_V_FHz_f9CIK6Rx",
            "1_20xxewMNIaO31v06yvUwn-1bKUHaNFI",
            "1UGGBVhIgTx-JooGysreAQ4MV7PPZMBor",
            """photorealistic, high quality, vibrant colors, bright lighting, skin detail, BREAK
            1girl, 18 years old, athletic, blonde hair, brown eyes, fair skin, slight smile.
            Style: realistic photo, Canon DSLR, soft daylight.""",
            [2, 3.10, -0.90, -1.10, 1.75, 0.6, 0.65, 0.80],
        ),
        setting1_generate_data(
            "zoe_callahan",
            "186Q9YFs1mQjFb0w6dM5cBR-c6BLfKxtI",
            "1AYHYcV3Frcm4bJyth2-5HWWBPdJyjhsQ",
            "1dg5pCLxK-SR1IlXpDjdJ6gQATT5ieg8v",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, blonde hair, brown eyes, tanned skin.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            [2, 2.65, -0.90, -0.85, 1.10, 0.7, 1.00, 0.80],
        ),
        setting1_generate_data(
            "brookenixon.xo",
            "1G9NXAMNU3MoqlV5lJ61g4yp_Nn-S6oBE",
            "1I3zaf77Z8OPu54LAN-qCqchxw7SDaxyj",
            "1tsI__nne0q6WSiL_BBWQ_gjiND_49MXd",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, blonde hair, brown eyes, tanned skin.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            [2, 1.9, -0.90, -0.85, 1.60, 1.20, 0.54, 0.80],
        ),
        setting1_generate_data(
            "giablake.xo",
            "1livvaka3OSpra5-7yMTivPc1gqxNgAnO",
            "1_Yf7uQlzVD_dv8bdqnCIYtDspo1FcVrs",
            "13CkgffWkQm20Qb4aYopS6Fxw6AgurShu",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, brown hair, blue eyes, pale skin.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            [2, 2.10, -0.90, -1.70, 1.50, 1.00, 1.00, 0.50],
        ),
        setting1_generate_data(
            "sierravexley",
            "12bi_ufYXj71QzV1jTHTSjYmAjPr2Utky",
            "1Hcw9aO89wyw4dco86kt5RRCC-Ue8Rebo",
            "1SNri9MEsRnJz9NF3YdJdub6h2X0efssM",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, brown hair, blue eyes, tanned skin, ponytail.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            [2, 1.60, -0.90, -1.70, 2.80, 1.00, 2.65, 0.80],
        ),
        setting1_generate_data(
            "roxie_foxx.xo",
            "1frrIY9choLe4w_pfcdTgZRG5dBmWs6Ov",
            "1TY7NBqaOk8uWVNH2Jo-4zEBh-_5w2KZg",
            "1Uu3vxmWFAOETfIRZJYMcj045fKNwj6aq",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, blonde hair, brown eyes, tanned skin.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            [2, 1.60, -0.90, -1.70, 1.75, 1.00, 0.00, 0.80],
        ),
        setting1_generate_data(
            "auroravaux.xo",
            "16_Dqz5eZgLmPniUW9_hIO2jqXdlMIHTX",
            "1UEoNZl90HGS7TpYGyKFIt6n2YyZT-Nfm",
            "1Fr0-5uJXtU6jXT8PPp4stKOHt5x3zfCR",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, blonde hair, tanned skin.
            Style: Instagram photo style, Canon DSLR, bright sunlight.""",
            [2, 0.00, -0.90, -1.70, 3.00, 1.00, 1.80, 0.80],
        ),
        setting1_generate_data(
            "skylalure",
            "112Dq-nCfS5IyazjXYxWIwhyaELT1VaCN",
            "1RhqUu5g1GGSE88Pyauil0Q0LjcPaKh5_",
            "1peAoxGyGn5tUHXxgOP5kKyWWOVhA6g5A",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, blonde hair, blue eyes, tanned skin.
            Style: Instagram photo style, Canon DSLR, bright sunlight.""",
            [2, 4.15, -0.90, -1.50, 1, 0.9, 0.05, 0.80],
        ),
        setting1_generate_data(
            "zara_devaux",
            "1XKaaQcqG_H0vyZ3t_aYqysrt6M0rRkHj",
            "1-eiSF72oH8-10yWsRQSjX3pjMXJYagb7",
            "12u5Vuh9QS-07LjdwdPNl6Iy1YQKEIqig",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, golden blonde hair, blue eyes, tanned skin.
            Style: Instagram photo style, Canon DSLR, bright sunlight.""",
            [2, 2.60, -0.90, -0.60, 0.45, 0.8, 0.95, 1.00],
        ),
        setting1_generate_data(
            "alinaquinn.xo",
            "1jm7i_DETYLUxV3QTksxDChKxbvvgBMFi",
            "1JkeqhnUHoc2eTJo88izHbARKSIEkyqLq",
            "113dX5DMf2r6uGQjqK3DWHvtFtAXcK4Eh",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, blonde hair, blue eyes, tanned skin.
            Style: Instagram photo style, Canon DSLR, bright sunlight.""",
            [2, 2.60, -0.90, -1.70, 1.50, 1.20, 1.50, 1.00],
        ),
        setting1_generate_data(
            "noavexen",
            "12taTvyKKUixwx6UOlJBFBXvKsvgLCOGR",
            "1BkRkjzVsEDlRoUvVwri4O0v2uq7Oym6P",
            "1eRbDvPlsi7b3HVwXBAihD8KWHjuP5ghe",
            """photorealistic, high quality, BREAK
            1girl, 18 years old, brown hair, green eyes, tan skin, smiling.""",
            [2, 2.4, -0.90, -1.40, 1.8, 1, 3, 1.00],
        ),
        setting1_generate_data(
            "lexalennix",
            "1rsnoyN7gq6S6cAd2rehgjfA2ZkzOcv5r",
            "1wTyGE4QjmvdEuqR7cuDwdH326_E84ZhJ",
            "1L5F1-EGt-TF0KewvTmeHGXzBMhDoWIvQ",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, brunette hair, green eyes, tanned skin.
            Style: Instagram photo style, Canon DSLR, bright sunlight.""",
            [2, 1.70, -0.90, -0.95, 0.95, 1.00, 0.05, 0.40],
        ),
        setting1_generate_data(
            "gia_prescott.xo",
            "15Rk4JipANNP26fxCcAV9CG7s8kDHUEM5",
            "1_5fFdQhUX_H5wLYLcp-dtppatIbfqDgQ",
            "1SvNkrxwyMsL0o9a-Cv-zgU2L05ixGWQy",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic, brunette hair, green eyes, tanned skin.
            Style: Instagram photo, Canon DSLR, bright sunlight""",
            [2, 1.70, -0.90, 1.40, 0.95, 1.00, 0.05, 0.80],
        ),
        setting1_generate_data(
            "daisyknoxen",
            "1vCXqB8f9t7WoQgTArcRvuN715zb32Rwx",
            "1mvr4PAOQ5RiZDdCDlDZtRTQVl35CTbUi",
            "1jzdn8A7Os-5HNJPOFcB-1cfdDJwSS40R",
            """photorealistic portrait of 18-year-old athletic redhead girl, tanned skin, modest clothing.
            Style: Instagram photo style, Canon DSLR, bright sunlight""",
            [2, 2.60, -0.90, -1.70, 0.05, 1.00, 4.85, 1.00],
        ),
        setting1_generate_data(
            "selinavoux",
            "1aQlirsy6EizF1yJ80VrIrRyx7dpsfWS2",
            "1_3wig40elwe66lAcrWqosUJYLyCR4P48",
            "10fL0AwVGA-uVxaG3q7R8Olsme2qjq7nC",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18, athletic, black hair, green eyes, pale skin.
            Style: Instagram photo, Canon DSLR, bright sunlight""",
            [2, 3.2, -0.90, -0.25, 1.5, 1.50, 0.10, 0.75],
        ),
        setting1_generate_data(
            "thaliavonn",
            "1ZO5LBmx-2p-irIOmVJRk5OLAgV9p9lWl",
            "15FKDsNIlKJvuRAfibAWCJoTg2AZ30VId",
            "1bLpDeRA7iYelm3QanF4UX1_FAWX-PbNY",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, blonde hair, blue eyes, tanned skin.
            Style: Instagram photo style, Canon DSLR, bright sunlight.""",
            [2, 1.10, -0.90, 0.35, 2.10, 1.00, 0.95, 1.00],
        ),
        setting1_generate_data(
            "adelinedior",
            "1wOcyvh3JVmv60SE2EjmfdpRQ3LWXcxHA",
            "1z-DL3bUbBQckmyWkNUfTj6oHQwuaSvFT",
            "1rKyWYuG0P4ScPFYp7pY41MAov8R62TKo",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, blonde hair, blue eyes, tanned skin.
            Style: Instagram photo style, Canon DSLR, bright sunlight.""",
            [2, 1.75, -0.90, -1.70, 0.10, 1.00, 0.10, 1.00],
        ),
        setting1_generate_data(
            "naomiruelle",
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
            "1uvYUlkG_A902uAmYwNWlXcqbYRo4hA07",
            "1LCR_JQEg2JIisADrnochKASReWbUCfrb",
            "18dssne4ftnQl6bwpY9QYj01UIp69HFbp",
            """photorealistic, high quality, BREAK
            1girl, 18 years old, blonde hair, green eyes, tan skin, smiling.""",
            [2, 3.10, -0.90, -1.70, 1.50, 0.9, 1.00, 0.40],
        ),
        setting1_generate_data(
            "sasharoxelle",
            "1CC3xxDdpYqmDH-4Bm-HVA32EghXdgZlK",
            "1scBkcxWIWasoo84FTO2M_VVb_4bnqIYX",
            "14Q0ENXHYlVVV7Xm173D6C9oNQ_4O6jo5",
            """photorealistic, high quality, BREAK
            1girl, 18 years old, brown hair, blue eyes, tan skin, smiling.""",
            [2, 1.00, -0.90, -0.35, 2.5, 1.00, 1.60, 0.55, 1.95],
        ),
    ]

    if settings.MOCK_IMAGES_MODE:
        dataArray = dataArray[:1]

    return dataArray
