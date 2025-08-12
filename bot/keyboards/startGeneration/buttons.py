from aiogram.types import InlineKeyboardButton


# Функция для выдавания кнопок с выбором типа генерации
def getGenerationsTypeButtons(
    prefix: str,
    with_work_generation: bool = True,
    rewrite_prompt: bool = False,
):
    inline_buttons = []

    if with_work_generation:
        inline_buttons.append(
            [
                InlineKeyboardButton(
                    text="⚡️ Work generation",
                    callback_data=f"{prefix}|work",
                ),
            ],
        )

    if rewrite_prompt:
        inline_buttons.append(
            [
                InlineKeyboardButton(
                    text="📹 Rewrite prompt",
                    callback_data=f"rewrite_prompt|{prefix.split('|')[1]}",
                ),
            ],
        )

    return inline_buttons
