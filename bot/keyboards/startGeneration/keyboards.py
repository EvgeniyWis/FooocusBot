from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.constants import MULTI_IMAGE_NUMBER
from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)
from bot.keyboards.startGeneration.buttons import getGenerationsTypeButtons


# Инлайн-клавиатура для выбора количества генераций
def generationsTypeKeyboard(
    with_work_generation: bool = True,
    with_video_from_image_generation: bool = True,
):
    inline_keyboard = getGenerationsTypeButtons(
        "generations_type",
        with_work_generation,
    )

    if with_video_from_image_generation:
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


def selectImageKeyboard(
    model_name: str,
    group_number: str,
    image_number: int,
    generation_id: str,
):
    inline_keyboard = []

    for i in range(1, image_number + 1, 2):
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{i}",
                    callback_data=f"select_image|{model_name}|{group_number}|{i}|{generation_id[:8]}",
                ),
                InlineKeyboardButton(
                    text=f"{i + 1}",
                    callback_data=f"select_image|{model_name}|{group_number}|{i + 1}|{generation_id[:8]}",
                ),
            ],
        )

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="🔄 Перегенерировать",
                callback_data=f"select_image|{model_name}|{group_number}|regenerate|{generation_id[:8]}",
            ),
        ]
    )
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="🔄 Перегенерировать с новым промптом",
                callback_data=f"select_image|{model_name}|{group_number}|prompt_regen|{generation_id[:8]}",
            ),
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


# Инлайн-клавиатура для выбора группы
def selectGroupKeyboard():
    inline_keyboard = []
    dataArrays = getAllDataArrays()

    for i in range(1, len(dataArrays)):
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"Группа {i}",
                    callback_data=f"select_group|{i}",
                ),
            ],
        )

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="Все группы",
                callback_data="select_group|all",
            ),
        ],
    )

    # Генерация конкретной модели
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="🔄 Индивидуальная генерация",
                callback_data="select_group|specific_model",
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
                    text="1️⃣ Один промпт + рандомайзер 🎲",
                    callback_data="write_prompt_type|one",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="✨ Уникальный промпт",
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
    group_number: str,
    image_number: int,
    selected_indexes: list[int],
    generation_id: str,
):
    # Первое изображение (index=0) - референсное, поэтому показываем кнопки с 1 по 9
    inline_keyboard = []
    for i in range(1, min(image_number, MULTI_IMAGE_NUMBER) + 1, 2):
        row = []
        for j in [i, i + 1]:
            if j > MULTI_IMAGE_NUMBER:
                continue
            idx = j
            selected = idx in selected_indexes
            text = f"{j} {'✅' if selected else ''}"
            row.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=f"select_multi_image|{model_name}|{group_number}|{idx}",
                ),
            )
        if row:
            inline_keyboard.append(row)

    short_generation_id = generation_id[:8]
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="Готово",
                callback_data=f"multi_image_done|{model_name}|{group_number}|{short_generation_id}",
            ),
        ],
    )
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="🔄 Перегенерировать",
                callback_data=f"select_image|{model_name}|{group_number}|regenerate|{short_generation_id}",
            ),
        ],
    )
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="🔄 Перегенерировать с новым промптом",
                callback_data=f"select_image|{model_name}|{group_number}|prompt_regen|{short_generation_id}",
            ),
        ],
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def done_typing_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Готово",
                    callback_data="done_typing",
                ),
            ],
        ],
    )


def select_type_specific_generation():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="1️⃣ Обычная",
                    callback_data="specific_generation|one_prompt",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔢 С уникальным промптом",
                    callback_data="specific_generation|more_prompts",
                ),
            ],
        ],
    )


# Клавиатура, когда все изображения успешно сохранены
def all_images_successfully_saved_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✨ Сгенерировать все видео по 1 промпту",
                    callback_data="generate_video_by_one_prompt",
                ),
            ],
        ],
    )
