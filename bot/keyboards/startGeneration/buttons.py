from aiogram.types import InlineKeyboardButton


# Функция для выдавания кнопок с выбором типа генерации
def getGenerationsTypeButtons(
    prefix: str,
    with_test_generation: bool = True,
    with_work_generation: bool = True,
    rewrite_prompt: bool = False,
):
    inline_buttons = []

    if with_work_generation:
        inline_buttons.append(
            [
                InlineKeyboardButton(
                    text="⚡️ Рабочая генерация",
                    callback_data=f"{prefix}|work",
                ),
            ],
        )

    if rewrite_prompt:
        inline_buttons.append(
            [
                InlineKeyboardButton(
                    text="📹 Переписать промпт",
                    callback_data=f"rewrite_prompt|{prefix.split('|')[1]}",
                ),
            ],
        )

    if with_test_generation:
        inline_buttons.append(
            [
                InlineKeyboardButton(
                    text="⚙️ Тестовая генерация",
                    callback_data=f"{prefix}|test",
                ),
            ],
        )

    return inline_buttons
