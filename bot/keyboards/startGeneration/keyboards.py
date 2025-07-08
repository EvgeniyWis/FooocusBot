from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.keyboards.startGeneration.buttons import getGenerationsTypeButtons


# Инлайн-клавиатура для выбора количества генераций
def generationsTypeKeyboard(
    with_work_generation: bool = True,
    with_test_generation: bool = True,
):
    inline_keyboard = getGenerationsTypeButtons(
        "generations_type",
        with_test_generation,
        with_work_generation,
    )
    inline_keyboard.extend(
        [
            [
                InlineKeyboardButton(
                    text="📹 Сгенерировать видео из изображения",
                    callback_data="generateVideoFromImage",
                ),
            ],
        ],
    )
    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    return kb


# Инлайн-клавиатура для выбора одного из изображений
def selectImageKeyboard(
    model_name: str,
    setting_number: str,
    image_number: int,
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
            ],
        )

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="🔄 Перегенерировать",
                callback_data=f"select_image|{model_name}|{setting_number}|regenerate",
            ),
        ],
    )
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="🔄 Перегенерировать с новым промптом",
                callback_data=f"select_image|{model_name}|{setting_number}|regenerate_with_new_prompt",
            ),
        ],
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
                    text=f"Настройка {i}",
                    callback_data=f"select_setting|{i}",
                ),
            ],
        )

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="Все настройки",
                callback_data="select_setting|all",
            ),
        ],
    )

    # Генерация конкретной модели
    if not is_test_generation:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text="🔄 Индивидуальная генерация",
                    callback_data="select_setting|specific_model",
                ),
            ],
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
                ),
            ],
            [
                InlineKeyboardButton(
                    text="✨ Уникальный промпт для каждой модели",
                    callback_data="write_prompt_type|unique",
                ),
            ],
        ],
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
                ),
            ],
        ],
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
                ),
            ],
            [
                InlineKeyboardButton(
                    text="✍️ Изменить промпт",
                    callback_data=f"select_setting|{setting_number}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="◀️ Назад",
                    callback_data="generations_type|test",
                ),
            ],
        ],
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
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🎲 Использовать рандомайзер",
                    callback_data="one_prompt_generation_type|random",
                ),
            ],
        ],
    )

    return kb


# Клавиатура для выбора режима генерации
def generationModeKeyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🖼 Мультивыбор",
                    callback_data="generation_mode|multi_select",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="1️⃣ Выбор одного фото",
                    callback_data="generation_mode|single_select",
                ),
            ],
        ],
    )


# Инлайн-клавиатура для мультивыборной генерации изображений
def selectMultiImageKeyboard(
    model_name: str,
    setting_number: str,
    image_number: int,
    selected_indexes: list[int],
):
    # Первое изображение (index=0) - референсное, поэтому показываем кнопки с 1 по 9
    inline_keyboard = []
    for i in range(1, min(image_number, 10), 2):
        row = []
        for j in [i, i + 1]:
            if j >= 10:
                continue
            idx = j
            selected = idx in selected_indexes
            text = f"{j} {'✅' if selected else ''}"
            row.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=f"select_multi_image|{model_name}|{setting_number}|{idx}",
                ),
            )
        if row:
            inline_keyboard.append(row)

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="Готово",
                callback_data=f"multi_image_done|{model_name}|{setting_number}",
            ),
        ],
    )
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="🔄 Перегенерировать",
                callback_data=f"select_image|{model_name}|{setting_number}|regenerate",
            ),
        ],
    )
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="🔄 Перегенерировать с новым промптом",
                callback_data=f"select_image|{model_name}|{setting_number}|regenerate_with_new_prompt",
            ),
        ],
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def admin_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👤 Профиль",
                    callback_data="user|profile",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📊 Лоры",
                    callback_data="user|lora_settings",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="👨‍💻 Промпты",
                    callback_data="user|prompts",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="📁 Веса для лор",
                    callback_data="user|lor_weights",
                ),
            ],
        ],
    )


def super_admin_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📊 Лоры",
                    callback_data="super_admin|lora_settings",
                ),
            ],
        ],
    )


def lora_admin_menu_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📋 Показать все LoRA",
                    callback_data="super_admin|show_loras",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="➕ Добавить LoRA",
                    callback_data="super_admin|add_lora",
                ),
            ],
        ],
    )


def lora_list_keyboard(loras: list[str]):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"{i+1}. {title}",
                    callback_data=f"super_admin|select_lora|{title}",
                ),
            ]
            for i, title in enumerate(loras)
        ],
    )


def selected_lora_action_keyboard(title: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✏️ Изменить",
                    callback_data=f"super_admin|edit_lora|{title}",
                ),
                InlineKeyboardButton(
                    text="🗑 Удалить",
                    callback_data=f"super_admin|delete_lora|{title}",
                ),
            ],
        ],
    )
