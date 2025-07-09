from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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


def user_registration_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📝 Создать профиль",
                    callback_data="user|create_profile",
                ),
            ],
        ],
    )


def user_loras_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📊 Настройки LoRA",
                    callback_data="user|change_lora_settings",
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
            [
                InlineKeyboardButton(
                    text="📁 Модели",
                    callback_data="super_admin|model_settings",
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


def lora_user_menu_keyboard(setting_number: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✏️ Изменить вес",
                    callback_data="user|edit_lora_weight",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🗑️ Удалить LoRA",
                    callback_data="user|delete_lora",
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data=f"user|select_setting|{setting_number}",
                ),
            ],
        ],
    )


def user_lora_list_keyboard(
    setting_number: int,
    user_loras: list,
    superadmin_titles: list,
) -> InlineKeyboardMarkup:
    buttons = []

    # Кнопки для удаления/редактирования веса для каждой лоры пользователя
    for l in user_loras:
        btn_text = f"LoRA ID {l['lora_id']} | Модель {l['model_name']} | Вес {l['weight']}"
        callback_data = f"user|select_lora|{setting_number}|{l['lora_id']}|{l['model_name']}"
        buttons.append(
            [InlineKeyboardButton(text=btn_text, callback_data=callback_data)],
        )

    # Кнопка добавить из супер-админских
    buttons.append(
        [
            InlineKeyboardButton(
                text="➕ Добавить LoRA",
                callback_data=f"user|add_lora|{setting_number}",
            ),
        ],
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def lora_admin_setting_selector_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Настройка {i}",
                    callback_data=f"super_admin|select_setting|{i}",
                ),
            ]
            for i in range(1, 5)
        ],
    )


def select_lora_keyboard(titles: list, setting_number: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=title,
                    callback_data=f"user|add_lora_confirm|{setting_number}|{title}",
                ),
            ]
            for title in titles
        ]
        + [
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data=f"user|select_setting|{setting_number}",
                ),
            ],
        ],
    )


def show_user_loras_keyboard(
    model_map: dict,
    user_loras: list,
    setting_number: int,
):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"LoRA ID {l['lora_id']} | Модель {model_map.get(l['model_id'], '❓')} | Вес {l['weight']}",
                    callback_data=f"user|select_lora|{setting_number}|{l['lora_id']}|{l['model_id']}",
                ),
            ]
            for l in user_loras
        ]
        + [
            [
                InlineKeyboardButton(
                    text="➕ Добавить LoRA",
                    callback_data=f"user|add_lora|{setting_number}",
                ),
            ],
        ],
    )


def select_model_for_lora_keyboard(models: list[dict], setting_number: int):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=model["name"],
                    callback_data=f"user|select_model_for_lora|{model['id']}",
                ),
            ]
            for model in models
        ]
        + [
            [
                InlineKeyboardButton(
                    text="🔙 Назад",
                    callback_data=f"user|add_lora|{setting_number}",
                ),
            ],
        ],
    )


def lora_list_keyboard(
    setting_number: int,
    loras: list[str],
) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=f"{i+1}. {title}",
                callback_data=f"super_admin|select_lora|{setting_number}|{title}",
            ),
        ]
        for i, title in enumerate(loras)
    ]

    buttons.append(
        [
            InlineKeyboardButton(
                text="➕ Добавить LoRA",
                callback_data=f"super_admin|add_lora|{setting_number}",
            ),
        ],
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def selected_lora_action_keyboard(setting_number: int, title: str):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✏️ Изменить",
                    callback_data=f"super_admin|edit_lora|{setting_number}|{title}",
                ),
                InlineKeyboardButton(
                    text="🗑 Удалить",
                    callback_data=f"super_admin|delete_lora|{setting_number}|{title}",
                ),
            ],
        ],
    )


def user_lora_setting_selector_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Настройка {i}",
                    callback_data=f"user|select_setting|{i}",
                ),
            ]
            for i in range(1, 5)
        ],
    )


def model_admin_setting_selector_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"Настройка {i}",
                    callback_data=f"super_admin|select_model_setting|{i}",
                ),
            ]
            for i in range(1, 5)
        ],
    )


def model_list_keyboard(
    setting_number: int,
    model_names: list[str],
) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=f"{i+1}. {name}",
                callback_data=f"super_admin|edit_model|{setting_number}|{name}",
            ),
            InlineKeyboardButton(
                text="🗑",
                callback_data=f"super_admin|delete_model|{setting_number}|{name}",
            ),
        ]
        for i, name in enumerate(model_names)
    ]

    buttons.append(
        [
            InlineKeyboardButton(
                text="➕ Добавить модель",
                callback_data=f"super_admin|add_model|{setting_number}",
            ),
        ],
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)
