from config import MOCK_MODE

from .generateData import setting1_generateData


# Функция для генерации массива данных для запроса для настройки 1
def setting1_getDataArray():
    # Массив дат с нужными параметрами для запроса
    dataArray = [
        setting1_generateData(
            "evanoir.xo",
            "1PxnsiuuUARM4uvCFvxzMb1zluQ5iwWlo",
            "1IsI6qcfCgNCt2qbeN3v430N8b8wQi4N9",
            """brown hair, blue eyes""",
            [2, 2.2, -0.9, -1.5, 1.5, 1.0, 1.5, 1.0, 0.35],
        ),
        setting1_generateData(
            "nika_saintclair",
            "1KtYtc3JSswLPQ3hu_G4obACI9rYjUaS0",
            "1yhljt9rN-dcSUbzzyd8OCLVn7xUI5xnp",
            """brown hair, blue eyes""",
            [2, 2.6, -0.9, -1.5, 1.5, 1.0, 1.70, 1.0],
        ),
        setting1_generateData(
            "chloemay",
            "1tpcOhP-d1YZ33RY3gQLjcz5exenweOBY",
            "1tKIrGKK17xPlCoXlkq0F6vvH_hyXjxXv",
            """brown hair, blue eyes""",
            [2, 2.9, -0.9, -1.7, 1.8, 1.0, 0.6, 0.8],
        ),
        setting1_generateData(
            "arialennix",
            "19XZemaTjt0TKkLjdh0LzogdfyDxaxWzC",
            "1JW-TTk1vlRGllaF_bVHMV6EOlqWpP-JN",
            """black hair, brown eyes""",
            [2, 1.80, -0.90, -1.70, 1.70, 1.00, 1.00, 0.80],
        ),
        setting1_generateData(
            "miaroxelle",
            "1eELjtIkSqwx64nLbih2hRUr-hDYxnSwh",
            "1g0XQOlJUHsKt3TNRVzhKPdLV6PDqb6Qv",
            """blonde hair, brown eyes, asian""",
            [2, 3.10, -0.90, -1.10, 1.00, 1.00, 1.00, 0.80],
        ),
        setting1_generateData(
            "brittany_cross.xo",
            "13hhG6B4dCPtb9CIPT56XykWf8KCopvD0",
            "1gDi92Np8hE8hML2wq-nB6uXt2REmuMIg",
            """blonde hair, brown eyes, slightly tanned skin""",
            [2, 3.10, -0.90, -1.10, 1.75, 0.7, 0.65, 0.80],
        ),
        setting1_generateData(
            "zoe_callahan",
            "1mwT7N1Ck5VdgJGS6eRYRQ97mczaLGi6b",
            "1YJB-tQCJVARYdWx23KatB-I8zXTDjZDn",
            """blonde hair, brown eyes, slightly tanned skin""",
            [2, 2.65, -0.90, -0.85, 1.40, 0.8, 1.00, 0.80],
        ),
        setting1_generateData(
            "brookenixon.xo",
            "1RlHfUuF_GrhgA5n985a8NqLkZgd5Y-kd",
            "1M5SChxLnMZAmQT72J-M4U8VsgOMZqALC",
            """blonde hair, brown eyes, slightly tanned skin""",
            [2, 1.9, -0.90, -0.85, 1.80, 1.00, 0.54, 0.80],
        ),
        setting1_generateData(
            "giablake.xo",
            "1beGL9f2ulLm6uYrZl2lc5QUAqZ6RBuzs",
            "1wW-J2e7WsXk7rTiCo6vGWwq3a2Gqqrf0",
            """brown hair, blue eyes, white skin""",
            [2, 2.10, -0.90, -1.70, 1.60, 1.00, 1.00, 0.50],
        ),
        setting1_generateData(
            "sierravexley",
            "1BpqfTJSNs8EbdyTTIBo0vvE5LgIsQvSH",
            "1jP2yTDmgpxXxdnmStmBcSMfG89_60ZdL",
            """brown hair, blue eyes, slightly tanned skin""",
            [2, 1.60, -0.90, -1.70, 3.00, 1.00, 2.65, 0.80],
        ),
        setting1_generateData(
            "roxie_foxx.xo",
            "11bl0KX0dl5RjUSOrINaqgowHbVCdLc5I",
            "1w1SPZZqKNL3-b0V4yqprqztePX7CvXo6",
            """blonde hair, brown eyes, slightly tanned skin""",
            [2, 1.60, -0.90, -1.70, 1.75, 1.00, 0.00, 0.80],
        ),
        setting1_generateData(
            "auroravaux.xo",
            "1Fp48pVc5EOf-UwK134eKlCRk7TGCnheR",
            "1lGN7b8J-0gPLhNDlGSlFgQg_pnL8VxpM",
            """blonde hair, brown eyes, slightly tanned skin""",
            [2, 0.00, -0.90, -1.70, 3.00, 1.00, 1.80, 0.80],
        ),
        setting1_generateData(
            "skylalure",
            "1R35YdfvQUTK1_wz1Wx9y7DRCkW4l2w10",
            "1K_eG4yHp1di75TR5OyeMNPzjyGX76Ua5",
            """blonde hair, blue eyes, slightly tanned skin""",
            [2, 4.15, -0.90, -1.50, 0.45, 1.00, 0.05, 0.80],
        ),
        setting1_generateData(
            "zara_devaux",
            "1G-cRYVvv0IRoKnOjvNuf10Dsa98RTXwG",
            "1KLnE5981AWAzKKaNY6darPgxIjS6UI9p",
            """blonde hair, blue eyes, slightly tanned skin""",
            [2, 2.60, -0.90, -0.60, 0.45, 1.00, 0.95, 1.00],
        ),
        setting1_generateData(
            "alinaquinn.xo",
            "1sTKaWqiH7nU0Jmwck-unGcCZkGID6a9a",
            "1fB6RvnWcjcj9rNXgsR-HXBkGzcxseUHp",
            """blonde hair, blue eyes, slightly tanned skin""",
            [2, 2.60, -0.90, -1.70, 1.50, 1.00, 1.50, 1.00],
        ),
        setting1_generateData(
            "noavexen",
            "1J39NtE4ovUiklcTW_t8NMZHTidCoTZNJ",
            "1jpaYrZUUKeh2sL5e3W3Nx0UaJX5fk9BB",
            """brown hair, green eyes, slightly tanned skin""",
            [2, 1.60, -0.90, -1.70, 1.55, 1.00, 3.00, 1.00],
        ),
        setting1_generateData(
            "lexalennix",
            "1ME0oexikdkzPqj1pJS-3z9NPY0ewAgVQ",
            "1y6qUi8iX5AMM1ns_B8B_j3HIIHH7reDC",
            """brown hair, green eyes, slightly tanned skin""",
            [2, 1.70, -0.90, -0.95, 0.95, 1.00, 0.05, 0.40],
        ),
        setting1_generateData(
            "gia_prescott.xo",
            "1cgjXUHiiAh8fYbFgFYzx6JYnrTBYX0cm",
            "1RDFZrbYp0NWFlhI4AGrb74QXwnVb6N0G",
            """brown hair, green eyes, tanned skin""",
            [2, 1.70, -0.90, 1.40, 0.95, 1.00, 0.05, 0.80],
        ),
        setting1_generateData(
            "daisyknoxen",
            "1BfBUv1bUHaGsWmBg8Oxv4r_wniQu2_VO",
            "1XReaJxJA2wRiJNbyjOZOdJC3lBNtpX5j",
            """dark orange hair, blue eyes, slightly tanned skin""",
            [2, 2.60, -0.90, -1.70, 0.05, 1.00, 4.85, 1.00],
            8,
        ),
        setting1_generateData(
            "selinavoux",
            "1GMY2IoGDR402Qfb-XHBIYHlj3vAxFypw",
            "1i78rV8aQfsTiSZZijmwg52wsQG-LModz",
            """black hair, green eyes, slightly tanned skin""",
            [2, 2.65, -0.90, -0.25, 0.70, 1.00, 0.10, 0.75],
        ),
        setting1_generateData(
            "thaliavonn",
            "1cQmMTefw1sWVRYooH3KmhHGyVb0njwpo",
            "1cchKR9pKlnkPcf0lZ1sEGoaE-Kf2CHQD",
            """blonde hair, blue eyes, slightly tanned skin""",
            [2, 1.10, -0.90, 0.35, 1.70, 1.00, 0.95, 1.00],
        ),
        setting1_generateData(
            "adelinedior",
            "1daQxeVSJWQGAVeUicUrgLj0hTwiT6Ws-",
            "1qwRI4JQ-1NzcH5Y0rwG0EyJzkeh8-T90",
            """blonde hair, blue eyes, slightly tanned skin""",
            [2, 1.75, -0.90, -1.70, 0.10, 1.00, 0.10, 1.00],
        ),
        setting1_generateData(
            "naomiruelle",
            "1EECavlAfyk-zA7iR0HAnDkH5H9qHMhbm",
            "1FBfwLfIDCiNPDQ7gF-14l5znrS_X49Xw",
            """blonde hair, green eyes, slightly tanned skin""",
            [2, 0.65, -0.90, -1.70, 3.65, 1, 1.2, 1.00],
        ),
        setting1_generateData(
            "miahazelton.xo",
            "1zHzqZi3BOprj7l7FiVs9riTHBUzI9Tat",
            "1RoBG69D7ZPkq2pgnSp6B7Rna63e_4sf2",
            """blonde hair, green eyes, slightly tanned skin""",
            [2, 3.10, -0.90, -1.70, 1.50, 1.00, 1.00, 0.40],
        ),
        setting1_generateData(
            "sasharoxelle",
            "1DbpoHrZcEbdVLtlGoQKev7Tdv9sE0vFY",
            "1k0GwrVzoluvXZ8_Z1ZtBq-xBAQVyijwh",
            """brown hair, blue eyes, slightly tanned skin""",
            [2, 1.00, -0.90, -0.35, 2.10, 1.00, 1.60, 0.55, 1.95],
        ),
    ]

    if MOCK_MODE:
        dataArray = dataArray[:1]

    return dataArray
