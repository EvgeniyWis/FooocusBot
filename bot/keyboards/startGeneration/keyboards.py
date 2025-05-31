from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from .buttons import getGenerationsTypeButtons


# Инлайн-клавиатура для выбора количества генераций
def generationsTypeKeyboard():
    inline_keyboard = getGenerationsTypeButtons("generations_type")
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="📹 Сгенерировать видео из изображения",
                callback_data="generateVideoFromImage",
            )
        ]
    )

    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    return kb


# Инлайн-клавиатура для выбора одного из изображений
def selectImageKeyboard(
    model_name: str, setting_number: str, image_number: int
):
    inline_keyboard = []

    for i in range(1, image_number + 1, 2):
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{i}",
                    callback_data=f"select_image|{model_name}|{setting_number}|{i}",
                ),
                InlineKeyboardButton(
                    text=f"{i + 1}",
                    callback_data=f"select_image|{model_name}|{setting_number}|{i + 1}",
                ),
            ]
        )

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="🔄 Перегенерировать",
                callback_data=f"select_image|{model_name}|{setting_number}|regenerate",
            )
        ]
    )
    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    return kb


# Инлайн-клавиатура для выбора настройки
def selectSettingKeyboard(is_test_generation: bool = False):
    inline_keyboard = []

    for i in range(1, 5):
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"Настройка {i}", callback_data=f"select_setting|{i}"
                )
            ]
        )

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="Все настройки", callback_data="select_setting|all"
            )
        ]
    )

    # Генерация конкретной модели
    if not is_test_generation:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text="🔄 Генерация конкретной модели",
                    callback_data="select_setting|specific_model",
                )
            ]
        )

    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    return kb


# Клавиатура для выбора режима написания промпта
def writePromptTypeKeyboard():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="1️⃣ Один промпт для всех моделей",
                    callback_data="write_prompt_type|one",
                )
            ],
            [
                InlineKeyboardButton(
                    text="✨ Уникальный промпт для кажд��й модели",
                    callback_data="write_prompt_type|unique",
                )
            ],
        ]
    )

    return kb


# Клавиатура для подтверждения написания уникального промпта для следующей модели
def confirmWriteUniquePromptForNextModelKeyboard():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✍️ Написать промпт",
                    callback_data="confirm_write_unique_prompt_for_next_model",
                )
            ],
        ]
    )

    return kb


# Клавиатура для тестирования с другими настройками
def testGenerationImagesKeyboard(setting_number: str):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔄 Сгенерировать с другими настройками",
                    callback_data="generations_type|test|prompt_exist",
                )
            ],
            [
                InlineKeyboardButton(
                    text="✍️ Изменить промпт",
                    callback_data=f"select_setting|{setting_number}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="◀️ ��азад", callback_data="generations_type|test"
                )
            ],
        ]
    )

    return kb


# Клавиатура для выбора режима при генерации с одним промптом
def onePromptGenerationChooseTypeKeyboard():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="⚖️ Статичный промпт",
                    callback_data="one_prompt_generation_type|static",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🎲 Использовать рандомайзер",
                    callback_data="one_prompt_generation_type|random",
                )
            ],
        ]
    )

    return kb


# Инлайн-клавиатура для перехода к этапу сохранения изображений
def saveImagesKeyboard():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💾 Этап сохранения изображений",
                    callback_data="save_images",
                )
            ]
        ]
    )

    return kb


# Инлайн-клавиатура при выборе для сохранения изображения
def saveImageKeyboard(model_name: str, setting_number: str):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💾 Сохранить изображение",
                    callback_data=f"save_image|{model_name}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Перегенерировать",
                    callback_data=f"select_image|{model_name}|{setting_number}|regenerate",
                )
            ],
        ]
    )

    return kb
