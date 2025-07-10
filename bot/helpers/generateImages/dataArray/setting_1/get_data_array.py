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
            "1PxnsiuuUARM4uvCFvxzMb1zluQ5iwWlo",
            "1IsI6qcfCgNCt2qbeN3v430N8b8wQi4N9",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 20 years old, athletic body, brown hair, blue eyes, natural skin texture.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            [2, 2.2, -0.9, -1.5, 1.5, 1.0, 1.85, 1.0, 0.35],
        ),
        setting1_generate_data(
            "nika_saintclair",
            "1KtYtc3JSswLPQ3hu_G4obACI9rYjUaS0",
            "1yhljt9rN-dcSUbzzyd8OCLVn7xUI5xnp",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 20 years old, athletic body, brown hair, blue eyes, natural skin texture.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            [2, 2.6, -0.9, -1.5, 1.4, 1.0, 1.40, 1.0],
        ),
        setting1_generate_data(
            "chloemay",
            "1tpcOhP-d1YZ33RY3gQLjcz5exenweOBY",
            "1tKIrGKK17xPlCoXlkq0F6vvH_hyXjxXv",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 20 years old, athletic body, brown hair, blue eyes, natural skin texture.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            [2, 2.9, -0.9, -1.7, 1.8, 0.9, 1, 0.8],
        ),
        setting1_generate_data(
            "arialennix",
            "19XZemaTjt0TKkLjdh0LzogdfyDxaxWzC",
            "1JW-TTk1vlRGllaF_bVHMV6EOlqWpP-JN",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 20 years old, skinny body, black hair, brown eyes, natural skin texture.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            [2, 1.80, -0.90, -1.70, 1.60, 1.00, 1.00, 0.80],
        ),
        setting1_generate_data(
            "miaroxelle",
            "1eELjtIkSqwx64nLbih2hRUr-hDYxnSwh",
            "1g0XQOlJUHsKt3TNRVzhKPdLV6PDqb6Qv",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, asian, 18 years old, athletic body, blonde hair, brown eyes, white skin.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            [2, 3.10, -0.90, -1.10, 0.9, 1.00, 1.00, 0.80],
        ),
        setting1_generate_data(
            "brittany_cross.xo",
            "13hhG6B4dCPtb9CIPT56XykWf8KCopvD0",
            "1gDi92Np8hE8hML2wq-nB6uXt2REmuMIg",
            """photorealistic, high quality, vibrant colors, bright lighting, skin detail, BREAK
            1girl, 18 years old, athletic, blonde hair, brown eyes, fair skin, slight smile.
            Style: realistic photo, Canon DSLR, soft daylight.""",
            [2, 3.10, -0.90, -1.10, 1.75, 0.6, 0.65, 0.80],
        ),
        setting1_generate_data(
            "zoe_callahan",
            "1mwT7N1Ck5VdgJGS6eRYRQ97mczaLGi6b",
            "1YJB-tQCJVARYdWx23KatB-I8zXTDjZDn",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, blonde hair, brown eyes, tanned skin.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            [2, 2.65, -0.90, -0.85, 1.10, 0.7, 1.00, 0.80],
        ),
        setting1_generate_data(
            "brookenixon.xo",
            "1RlHfUuF_GrhgA5n985a8NqLkZgd5Y-kd",
            "1M5SChxLnMZAmQT72J-M4U8VsgOMZqALC",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, blonde hair, brown eyes, tanned skin.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            [2, 1.9, -0.90, -0.85, 1.60, 1.20, 0.54, 0.80],
        ),
        setting1_generate_data(
            "giablake.xo",
            "1beGL9f2ulLm6uYrZl2lc5QUAqZ6RBuzs",
            "1wW-J2e7WsXk7rTiCo6vGWwq3a2Gqqrf0",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, brown hair, blue eyes, pale skin.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            [2, 2.10, -0.90, -1.70, 1.50, 1.00, 1.00, 0.50],
        ),
        setting1_generate_data(
            "sierravexley",
            "1BpqfTJSNs8EbdyTTIBo0vvE5LgIsQvSH",
            "1jP2yTDmgpxXxdnmStmBcSMfG89_60ZdL",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, brown hair, blue eyes, tanned skin, ponytail.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            [2, 1.60, -0.90, -1.70, 3.00, 1.00, 2.65, 0.80],
        ),
        setting1_generate_data(
            "roxie_foxx.xo",
            "11bl0KX0dl5RjUSOrINaqgowHbVCdLc5I",
            "1w1SPZZqKNL3-b0V4yqprqztePX7CvXo6",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, blonde hair, brown eyes, tanned skin, hourglass figure.
            Style: realistic photography, Canon DSLR, natural daylight.""",
            [2, 1.60, -0.90, -1.70, 1.75, 1.00, 0.00, 0.80],
        ),
        setting1_generate_data(
            "auroravaux.xo",
            "1Fp48pVc5EOf-UwK134eKlCRk7TGCnheR",
            "1lGN7b8J-0gPLhNDlGSlFgQg_pnL8VxpM",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, blonde hair, tanned skin, hourglass figure.
            Style: Instagram photo style, Canon DSLR, bright sunlight.""",
            [2, 0.00, -0.90, -1.70, 3.00, 1.00, 1.80, 0.80],
        ),
        setting1_generate_data(
            "skylalure",
            "1R35YdfvQUTK1_wz1Wx9y7DRCkW4l2w10",
            "1K_eG4yHp1di75TR5OyeMNPzjyGX76Ua5",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, blonde hair, blue eyes, tanned skin, hourglass figure.
            Style: Instagram photo style, Canon DSLR, bright sunlight.""",
            [2, 4.15, -0.90, -1.50, 0.7, 0.9, 0.05, 0.80],
        ),
        setting1_generate_data(
            "zara_devaux",
            "1G-cRYVvv0IRoKnOjvNuf10Dsa98RTXwG",
            "1KLnE5981AWAzKKaNY6darPgxIjS6UI9p",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, golden blonde hair, blue eyes, tanned skin, hourglass figure.
            Style: Instagram photo style, Canon DSLR, bright sunlight.""",
            [2, 2.60, -0.90, -0.60, 0.45, 0.8, 0.95, 1.00],
        ),
        setting1_generate_data(
            "alinaquinn.xo",
            "1sTKaWqiH7nU0Jmwck-unGcCZkGID6a9a",
            "1fB6RvnWcjcj9rNXgsR-HXBkGzcxseUHp",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, blonde hair, blue eyes, tanned skin, hourglass figure.
            Style: Instagram photo style, Canon DSLR, bright sunlight.""",
            [2, 2.60, -0.90, -1.70, 1.50, 1.20, 1.50, 1.00],
        ),
        setting1_generate_data(
            "noavexen",
            "1J39NtE4ovUiklcTW_t8NMZHTidCoTZNJ",
            "1jpaYrZUUKeh2sL5e3W3Nx0UaJX5fk9BB",
            """photorealistic, high quality, BREAK
            1girl, 18 years old, brown hair, green eyes, tan skin, smiling.""",
            [2, 2.4, -0.90, -1.40, 1.8, 1, 3, 1.00],
        ),
        setting1_generate_data(
            "lexalennix",
            "1ME0oexikdkzPqj1pJS-3z9NPY0ewAgVQ",
            "1y6qUi8iX5AMM1ns_B8B_j3HIIHH7reDC",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, brunette hair, green eyes, tanned skin, hourglass figure.
            Style: Instagram photo style, Canon DSLR, bright sunlight.""",
            [2, 1.70, -0.90, -0.95, 0.95, 1.00, 0.05, 0.40],
        ),
        setting1_generate_data(
            "gia_prescott.xo",
            "1cgjXUHiiAh8fYbFgFYzx6JYnrTBYX0cm",
            "1RDFZrbYp0NWFlhI4AGrb74QXwnVb6N0G",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic, brunette hair, green eyes, tanned skin, hourglass figure.
            Style: Instagram photo, Canon DSLR, bright sunlight""",
            [2, 1.70, -0.90, 1.40, 0.95, 1.00, 0.05, 0.80],
        ),
        setting1_generate_data(
            "daisyknoxen",
            "1BfBUv1bUHaGsWmBg8Oxv4r_wniQu2_VO",
            "1XReaJxJA2wRiJNbyjOZOdJC3lBNtpX5j",
            """photorealistic portrait of 18-year-old athletic redhead girl, hourglass figure, tanned skin, modest clothing.
            Style: Instagram photo style, Canon DSLR, bright sunlight""",
            [2, 2.60, -0.90, -1.70, 0.05, 1.00, 4.85, 1.00],
        ),
        setting1_generate_data(
            "selinavoux",
            "1GMY2IoGDR402Qfb-XHBIYHlj3vAxFypw",
            "1i78rV8aQfsTiSZZijmwg52wsQG-LModz",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18, athletic, black hair, green eyes, pale skin, hourglass figure.
            Style: Instagram photo, Canon DSLR, bright sunlight""",
            [2, 3.2, -0.90, -0.25, 1.5, 1.50, 0.10, 0.75],
        ),
        setting1_generate_data(
            "thaliavonn",
            "1cQmMTefw1sWVRYooH3KmhHGyVb0njwpo",
            "1cchKR9pKlnkPcf0lZ1sEGoaE-Kf2CHQD",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, blonde hair, blue eyes, tanned skin, hourglass figure.
            Style: Instagram photo style, Canon DSLR, bright sunlight.""",
            [2, 1.10, -0.90, 0.35, 2.10, 1.00, 0.95, 1.00],
        ),
        setting1_generate_data(
            "adelinedior",
            "1daQxeVSJWQGAVeUicUrgLj0hTwiT6Ws-",
            "1qwRI4JQ-1NzcH5Y0rwG0EyJzkeh8-T90",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic body, blonde hair, blue eyes, tanned skin, hourglass figure.
            Style: Instagram photo style, Canon DSLR, bright sunlight.""",
            [2, 1.75, -0.90, -1.70, 0.10, 1.00, 0.10, 1.00],
        ),
        setting1_generate_data(
            "naomiruelle",
            "1EECavlAfyk-zA7iR0HAnDkH5H9qHMhbm",
            "1FBfwLfIDCiNPDQ7gF-14l5znrS_X49Xw",
            """photorealistic, high quality, vibrant colors, skin detail, BREAK
            1girl, 18 years old, athletic, blonde hair, green eyes, tanned skin, hourglass figure.
            Style: Instagram photo style, Canon DSLR, bright sunlight""",
            [2, 0.65, -0.90, -1.70, 4, 1.25, 1.75, 1.00],
        ),
        setting1_generate_data(
            "miahazelton.xo",
            "1zHzqZi3BOprj7l7FiVs9riTHBUzI9Tat",
            "1RoBG69D7ZPkq2pgnSp6B7Rna63e_4sf2",
            """photorealistic, high quality, BREAK
            1girl, 18 years old, blonde hair, green eyes, tan skin, smiling.""",
            [2, 3.10, -0.90, -1.70, 1.50, 0.9, 1.00, 0.40],
        ),
        setting1_generate_data(
            "sasharoxelle",
            "1jMZnHt32aDHJZU7Ihr84b7eXlFi_M9mE",
            "1R8zwFg_U52IZPR-546-HZdtSw3DzrUWK",
            """photorealistic, high quality, BREAK
            1girl, 18 years old, brown hair, blue eyes, tan skin, smiling.""",
            [2, 1.00, -0.90, -0.35, 2.5, 1.00, 1.60, 0.55, 1.95],
        ),
    ]

    if settings.MOCK_IMAGES_MODE:
        dataArray = dataArray[:1]

    return dataArray
