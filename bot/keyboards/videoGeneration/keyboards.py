from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.keyboards.startGeneration.buttons import getGenerationsTypeButtons


# Инлайн-клавиатура для генерации видео
def generateVideoKeyboard(model_name: str, image_index: int):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
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
        ],
    )

    return kb


# Инлайн-клавиатура для выбора типа генерации видео
def generatedVideoKeyboard(prefix: str, with_test_generation: bool = True):
    inline_keyboard = getGenerationsTypeButtons(
        prefix,
        with_test_generation=with_test_generation,
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
                with_test_generation=False,
                rewrite_prompt=True,
            ),
        ],
    )

    return kb


# Инлайн-клавиатура для выбора корректности генерации видео
def videoCorrectnessKeyboard(
    model_name: str,
    image_index: int | None = None,
):
    
    if image_index is None:
        postfix = f"{model_name}"
    else:
        postfix = f"{model_name}|{image_index}"

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Сохранить видео",
                    callback_data=f"video_correctness|correct|{postfix}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔄 Перегенерировать с новым промптом",
                    callback_data=f"quick_video_generation|{postfix}",
                ),
            ],
        ],
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
