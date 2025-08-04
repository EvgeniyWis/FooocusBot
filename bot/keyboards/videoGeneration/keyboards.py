from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.keyboards.startGeneration.buttons import getGenerationsTypeButtons


# Инлайн-клавиатура для генерации видео
def generateVideoKeyboard(model_name: str, image_index: int, with_magnific_upscale: bool = True):
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text="⚡️ Генерация обычного видео",
                callback_data=f"quick_video_generation|{model_name}|{image_index}",
            ),
        ],
        [
            InlineKeyboardButton(
                text="🤖 Генерация NSFW видео",
                callback_data=f"generate_comfyui_video|{model_name}|{image_index}",
            ),
        ],
    ]

    if with_magnific_upscale:
        inline_keyboard.append(
            [InlineKeyboardButton(
                text="🪄 Использовать Magnific Upscaler",
                callback_data=f"magnific_upscale|{model_name}|{image_index}",
            )],
        )

    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    return kb


# Инлайн-клавиатура для выбора типа генерации видео
def generatedVideoKeyboard(prefix: str):
    inline_keyboard = getGenerationsTypeButtons(
        prefix,
    )

    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    return kb


# Инлайн-клавиатура для выбора типа генерации видео
def videoGenerationTypeKeyboard(
    model_name: str,
    image_index: int | None = None,
):
    if image_index is None:
        prefix = f"generate_video|{model_name}"
    else:
        prefix = f"generate_video|{model_name}|{image_index}"

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            *getGenerationsTypeButtons(
                prefix=prefix,
                with_work_generation=False,
                rewrite_prompt=True,
            ),
        ],
    )

    return kb


# Инлайн-клавиатура для выбора корректности генерации видео
def videoCorrectnessKeyboard(
    model_name: str,
    image_index: int | None = None,
    is_nsfw: bool = False,
    video_index: int | None = None,
    with_regenerate: bool = True,
):
    if is_nsfw:
        postfix = f"nsfw|{model_name}"
    else:
        postfix = f"{model_name}"

    if image_index is not None:
        postfix += f"|{image_index}"

    if video_index is not None:
        postfix += f"|{video_index}"

    inline_keyboard = [
            [
                InlineKeyboardButton(
                    text="✅ Сохранить видео",
                    callback_data=f"video_correctness|correct|{postfix}",
                ),
            ],
        ]

    if with_regenerate:
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text="🔄 Перегенерировать с новым промптом",
                    callback_data=f"quick_video_generation|{postfix}",
                ),
            ],
        )

    kb = InlineKeyboardMarkup(
        inline_keyboard=inline_keyboard,
    )

    return kb


def nsfw_video_generation_insert_length_video_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                    text="✅ Оставить по умолчанию",
                    callback_data="video_length_choice|default",
                )],
                [
                InlineKeyboardButton(
                    text="✒️ Ввести свою длительность",
                    callback_data="video_length_choice|input",
                )],
        ],
    )
    return keyboard


# Инлайн-клавиатура с кнопкой "✅ Готово" для прекращения сбора изображений для генерации видео
def img2video_done_send_images_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Готово", callback_data="img2video|done_send_images")],
        ],
    )
    return keyboard


# Инлайн-клавиатура для выбора типа ввода промпта в img2video
def choose_prompt_type_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📝 Один промпт для всех",
                    callback_data="img2video|prompt_type|one",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔤 Уникальный промпт для каждого",
                    callback_data="img2video|prompt_type|multi",
                ),
            ],
        ],
    )
    return keyboard


# Инлайн-клавиатура для завершения ввода промптов в img2video
def img2video_done_typing_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Готово",
                    callback_data="img2video|finish_prompt",
                ),
            ],
        ],
    )
    return keyboard