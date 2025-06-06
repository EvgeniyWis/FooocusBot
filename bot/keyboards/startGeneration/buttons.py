from aiogram.types import InlineKeyboardButton


# Функция для выдавания кнопок с выбором типа генерации
def getGenerationsTypeButtons(prefix: str, with_test_generation: bool = True, with_work_generation: bool = True):
    inline_buttons = []

    if with_work_generation:
        inline_buttons.append(
            [
                InlineKeyboardButton(
                    text="⚡️ Рабочая генерация", callback_data=f"{prefix}|work",
                ),
            ],
        )

    if with_test_generation:
        inline_buttons.append(
            [
                InlineKeyboardButton(
                    text="⚙️ Тестовая генерация", callback_data=f"{prefix}|test",
                ),
            ],
        )

    return inline_buttons
