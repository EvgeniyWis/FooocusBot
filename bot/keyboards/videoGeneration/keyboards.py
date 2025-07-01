from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.keyboards.startGeneration.buttons import getGenerationsTypeButtons


# Инлайн-клавиатура для генерации видео
def generateVideoKeyboard(model_name: str, image_index: int):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📹 Сгенерировать видео",
                    callback_data=f"start_generate_video|{model_name}|default",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="⚡️Генерация видео с промптом",
                    callback_data=f"quick_video_generation|{model_name}|{image_index}",
                ),
            ],
        ],
    )

    return kb


# Инлайн-клавиатура при отправки примера видео с промптом с выбором типа генерации и возможности написания кастомного промпта
def videoWritePromptKeyboard(model_name: str):
    prefix = f"generate_video_mode|{model_name}"

    inline_keyboard = [
        [
            InlineKeyboardButton(
                text="✒️ Написать свой промпт",
                callback_data=f"{prefix}|write_prompt",
            ),
        ],
    ]

    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

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
    with_test_generation: bool = False,
    rewrite_prompt: bool = False,
):
    prefix = f"generate_video|{model_name}"

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            *getGenerationsTypeButtons(
                prefix=prefix,
                with_test_generation=with_test_generation,
                rewrite_prompt=rewrite_prompt,
            ),
        ],
    )

    return kb


# Инлайн-клавиатура для выбора корректности генерации видео
def videoCorrectnessKeyboard(model_name: str, is_quick_generation: bool = False):
    if is_quick_generation:
        postfix = "quick"
    else:
        postfix = "default"

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Сохранить видео",
                    callback_data=f"video_correctness|correct|{model_name}",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="❌ Перегенерировать видео",
                    callback_data=f"start_generate_video|{model_name}|{postfix}",
                ),
            ],
        ],
    )

    return kb


# Инлайн-клавиатура для выбора режима генерации видео
def videoGenerationModeKeyboard(model_name: str):
    prefix = f"generate_video_mode|{model_name}"

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✒️ Написать свой промпт",
                    callback_data=f"{prefix}|write_prompt",
                ),
            ],
            # TODO: режим генерации видео с видео-примерами временно отключен
            # [InlineKeyboardButton(text='⚙️ Использовать заготовленные примеры', callback_data=f'{prefix}|use_examples')]
        ],
    )

    return kb
