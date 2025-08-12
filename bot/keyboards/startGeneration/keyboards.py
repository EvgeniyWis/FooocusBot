from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.app.config.constants import MULTI_IMAGE_NUMBER
from bot.helpers.generateImages.dataArray.getAllDataArrays import (
    getAllDataArrays,
)
from bot.keyboards.startGeneration.buttons import getGenerationsTypeButtons


# Inline keyboard for selecting the number of generations
def generationsTypeKeyboard(
    with_work_generation: bool = True,
    with_video_from_image_generation: bool = True,
):
    inline_keyboard = getGenerationsTypeButtons(
        "generations_type",
        with_work_generation,
    )
    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    return kb


def selectImageKeyboard(
    model_name: str,
    group_number: str,
    image_number: int,
    job_id: str,
    model_key: str = None,
):
    inline_keyboard = []

    # Формируем полный ключ модели для callback data
    full_model_key = f"{model_name}_{model_key}" if model_key else model_name

    for i in range(1, image_number + 1, 2):
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=f"{i}",
                    callback_data=f"select_image|{full_model_key}|{group_number}|{i}|{job_id[:8]}",
                ),
                InlineKeyboardButton(
                    text=f"{i + 1}",
                    callback_data=f"select_image|{full_model_key}|{group_number}|{i + 1}|{job_id[:8]}",
                ),
            ],
        )

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="🔄 Перегенерировать",
                callback_data=f"select_image|{full_model_key}|{group_number}|regenerate|{job_id[:8]}",
            ),
        ]
    )
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="🔄 Перегенерировать с новым промптом",
                callback_data=f"select_image|{full_model_key}|{group_number}|prompt_regen|{job_id[:8]}",
            ),
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


# Inline keyboard for selecting a group
def selectGroupKeyboard():
    inline_keyboard = []
    dataArrays = getAllDataArrays()

    for i in range(1, len(dataArrays)):
        inline_keyboard.append(
            [
                InlineKeyboardButton(
                                            text=f"Group {i}",
                    callback_data=f"select_group|{i}",
                ),
            ],
        )

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                                        text="All groups",
                callback_data="select_group|all",
            ),
        ],
    )

    # Generation of a specific model
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                                        text="🔄 Individual generation",
                callback_data="select_group|specific_model",
            ),
        ],
    )

    kb = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    return kb


# Keyboard to choose prompt writing mode
def writePromptTypeKeyboard():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                                            text="1️⃣ One prompt + randomizer 🎲",
                    callback_data="write_prompt_type|one",
                ),
            ],
            [
                InlineKeyboardButton(
                                            text="✨ Unique prompt",
                    callback_data="write_prompt_type|unique",
                ),
            ],
        ],
    )

    return kb


# Keyboard to confirm writing a unique prompt for the next model
def confirmWriteUniquePromptForNextModelKeyboard():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                                            text="✍️ Write a prompt",
                    callback_data="confirm_write_unique_prompt_for_next_model",
                ),
            ],
        ],
    )

    return kb


# Keyboard to choose mode for single-prompt generation
def onePromptGenerationChooseTypeKeyboard():
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                                            text="⚖️ Static prompt",
                    callback_data="one_prompt_generation_type|static",
                ),
            ],
            [
                InlineKeyboardButton(
                                            text="🎲 Use randomizer",
                    callback_data="one_prompt_generation_type|random",
                ),
            ],
        ],
    )

    return kb


# Keyboard to select generation mode
def generationModeKeyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                                            text="🖼 Multi-select",
                    callback_data="generation_mode|multi_select",
                ),
            ],
            [
                InlineKeyboardButton(
                                            text="1️⃣ Select one photo",
                    callback_data="generation_mode|single_select",
                ),
            ],
        ],
    )


# Inline keyboard for multi-select image generation
def selectMultiImageKeyboard(
    model_name: str,
    group_number: str,
    image_number: int,
    selected_indexes: list[int],
    job_id: str,
    model_key: str = None,
):
    # Формируем полный ключ модели для callback data
    full_model_key = f"{model_name}_{model_key}" if model_key else model_name
    
    # The first image (index=0) is the reference, so show buttons from 1 to MULTI_IMAGE_NUMBER
    inline_keyboard = []
    short_job_id = job_id[:8]
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
                    callback_data=f"select_multi_image|{full_model_key}|{group_number}|{idx}|{short_job_id}",
                ),
            )
        if row:
            inline_keyboard.append(row)

    inline_keyboard.append(
        [
            InlineKeyboardButton(
                                    text="Done",
                callback_data=f"multi_image_done|{full_model_key}|{group_number}|{short_job_id}",
            ),
        ],
    )
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="🔄 Перегенерировать",
                callback_data=f"select_image|{full_model_key}|{group_number}|regenerate|{short_job_id}",
            ),
        ],
    )
    inline_keyboard.append(
        [
            InlineKeyboardButton(
                text="🔄 Перегенерировать с новым промптом",
                callback_data=f"select_image|{full_model_key}|{group_number}|prompt_regen|{short_job_id}",
            ),
        ],
    )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def done_typing_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Done",
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
                                            text="1️⃣ Regular",
                    callback_data="specific_generation|one_prompt",
                ),
            ],
            [
                InlineKeyboardButton(
                                            text="🔢 With unique prompt",
                    callback_data="specific_generation|more_prompts",
                ),
            ],
        ],
    )


# Keyboard shown when all images are successfully saved
def all_images_successfully_saved_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                                            text="✨ Generate all videos with one prompt",
                    callback_data="generate_video_by_one_prompt",
                ),
            ],
        ],
    )
