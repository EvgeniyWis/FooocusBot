import re

from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from states.AdminState import UserAccessStates
from states.StartGenerationState import LoraEditStates, ModelEditStates
from utils.handlers.messages import safe_edit_message

from bot.factory.user_factory import get_user_settings_service
from bot.InstanceBot import router
from bot.keyboards.users.keyboards import (
    lora_admin_setting_selector_keyboard,
    lora_list_keyboard,
    model_admin_setting_selector_keyboard,
    model_list_keyboard,
    selected_lora_action_keyboard,
)


async def handle_lora_menu(callback: types.CallbackQuery):
    await safe_edit_message(
        callback.message,
        "⚙️ Выберите настройку:",
        reply_markup=lora_admin_setting_selector_keyboard(),
    )


async def handle_select_setting(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    _, _, setting_str = callback.data.split("|")
    setting_number = int(setting_str)
    await state.update_data(setting_number=setting_number)

    service = await get_user_settings_service()
    loras = await service.superadmin_get_all_loras(setting_number)
    lora_titles = [l["title"] for l in loras]

    await safe_edit_message(
        callback.message,
        f"📋 Список LoRA моделей для настройки {setting_number}:",
        reply_markup=lora_list_keyboard(setting_number, lora_titles),
    )


async def handle_lora_selected(callback: types.CallbackQuery):
    _, _, setting_str, title = callback.data.split("|", 3)
    setting_number = int(setting_str)

    await safe_edit_message(
        callback.message,
        f"📌 Вы выбрали LoRA: *{title}*\n🔧 Настройка: {setting_number}",
        parse_mode="Markdown",
        reply_markup=selected_lora_action_keyboard(setting_number, title),
    )


async def handle_lora_delete(callback: types.CallbackQuery):
    _, _, setting_str, title = callback.data.split("|", 3)
    setting_number = int(setting_str)
    service = await get_user_settings_service()
    await service.superadmin_delete_lora(title, setting_number)
    await safe_edit_message(
        callback.message,
        f"🗑 LoRA `{title}` удалена (настройка {setting_number}).",
        parse_mode="Markdown",
    )


async def handle_lora_edit(callback: types.CallbackQuery, state: FSMContext):
    _, _, setting_str, title = callback.data.split("|", 3)
    await state.set_state(LoraEditStates.waiting_for_new_title)
    await state.update_data(old_title=title, setting_number=int(setting_str))
    await safe_edit_message(
        callback.message,
        f"✏️ Введите новое название для LoRA `{title}`:",
        parse_mode="Markdown",
    )


@router.message(LoraEditStates.waiting_for_new_title)
async def process_lora_title_edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    old_title = data["old_title"]
    setting_number = data["setting_number"]
    new_title = message.text.strip()

    if not new_title:
        await message.answer(
            "❌ Название не может быть пустым. Повторите попытку.",
        )
        return

    service = await get_user_settings_service()
    await service.superadmin_rename_lora(old_title, setting_number, new_title)

    await message.answer(
        f"✅ LoRA `{old_title}` переименована в `{new_title}` (настройка {setting_number}).",
        parse_mode="Markdown",
    )
    await state.clear()


async def handle_add_lora(callback: types.CallbackQuery, state: FSMContext):
    _, _, setting_str = callback.data.split("|", 2)
    setting_number = int(setting_str)

    await state.set_state(LoraEditStates.waiting_for_add_title)
    await state.update_data(setting_number=setting_number)

    await safe_edit_message(
        callback.message,
        f"➕ Введите название новой LoRA (настройка {setting_number}):",
    )


async def process_lora_add(message: types.Message, state: FSMContext):
    new_title = message.text.strip()
    if not new_title:
        await message.answer(
            "❌ Название не может быть пустым. Повторите попытку.",
        )
        return

    data = await state.get_data()
    setting_number = data.get("setting_number")
    if setting_number is None:
        await message.answer(
            "⚠️ Не выбрана настройка. Повторите процесс добавления через админ-панель.",
        )
        await state.clear()
        return

    service = await get_user_settings_service()
    await service.superadmin_add_lora(new_title, setting_number)

    await message.answer(
        f"✅ LoRA `{new_title}` добавлена (настройка {setting_number}).",
        parse_mode="Markdown",
    )
    await state.clear()


async def handle_model_menu(callback: types.CallbackQuery):
    await safe_edit_message(
        callback.message,
        "⚙️ Выберите настройку для управления моделями:",
        reply_markup=model_admin_setting_selector_keyboard(),
    )


async def handle_model_setting_selected(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    _, _, setting_str = callback.data.split("|")
    setting_number = int(setting_str)
    await state.update_data(setting_number=setting_number)

    service = await get_user_settings_service()
    models = await service.repo.superadmin_get_models_by_setting(
        setting_number,
    )
    model_names = [m["name"] for m in models]

    await safe_edit_message(
        callback.message,
        f"📋 Модели для настройки {setting_number}:",
        reply_markup=model_list_keyboard(setting_number, model_names),
    )


async def handle_add_model(callback: types.CallbackQuery, state: FSMContext):
    _, _, setting_str = callback.data.split("|")
    await state.set_state(ModelEditStates.waiting_for_model_name)
    await state.update_data(setting_number=int(setting_str))

    await safe_edit_message(
        callback.message,
        "➕ Введите название новой модели:",
    )


async def process_add_model_name(message: types.Message, state: FSMContext):
    data = await state.get_data()
    setting_number = data["setting_number"]
    model_name = message.text.strip()

    if not model_name:
        await message.answer("❌ Название не может быть пустым.")
        return

    service = await get_user_settings_service()
    await service.repo.superadmin_add_model(model_name, setting_number)
    await message.answer(
        f"✅ Модель `{model_name}` добавлена (настройка {setting_number}).",
        parse_mode="Markdown",
    )
    await state.clear()


async def handle_edit_model(callback: types.CallbackQuery, state: FSMContext):
    _, _, setting_str, old_name = callback.data.split("|", 3)
    await state.set_state(ModelEditStates.waiting_for_model_rename)
    await state.update_data(
        old_model_name=old_name,
        setting_number=int(setting_str),
    )

    await safe_edit_message(
        callback.message,
        f"✏️ Введите новое название для модели `{old_name}`:",
        parse_mode="Markdown",
    )


async def process_model_rename(message: types.Message, state: FSMContext):
    data = await state.get_data()
    old_name = data["old_model_name"]
    setting_number = data["setting_number"]
    new_name = message.text.strip()

    if not new_name:
        await message.answer("❌ Название не может быть пустым.")
        return

    service = await get_user_settings_service()
    await service.repo.superadmin_rename_model(
        old_name,
        new_name,
        setting_number,
    )
    await message.answer(
        f"✅ Модель `{old_name}` переименована в `{new_name}`.",
        parse_mode="Markdown",
    )
    await state.clear()


async def handle_delete_model(
    callback: types.CallbackQuery,
    state: FSMContext,
):
    _, _, setting_str, model_name = callback.data.split("|", 3)
    setting_number = int(setting_str)
    service = await get_user_settings_service()
    await service.repo.superadmin_delete_model(model_name, setting_number)

    await safe_edit_message(
        callback.message,
        f"🗑 Модель `{model_name}` удалена (настройка {setting_number}).",
        parse_mode="Markdown",
    )


def extract_user_id(message: types.Message) -> int | None:
    if message.forward_from:
        return message.forward_from.id

    text = message.text.strip()

    if text.isdigit():
        return int(text)

    match = re.search(r"tg://user\?id=(\d+)", text)
    if match:
        return int(match.group(1))

    return None


async def handle_add_user(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(UserAccessStates.waiting_for_add_user)
    await safe_edit_message(
        callback.message,
        "➕ Перешлите сообщение от пользователя ИЛИ отправьте `tg_id`, ИЛИ `tg://user?id=123456789`:",
    )


async def process_add_user(message: types.Message, state: FSMContext):
    tg_id = extract_user_id(message)
    if tg_id is None:
        await message.answer(
            "❌ Не удалось определить ID пользователя. "
            "Попробуйте другой способ (например, отправьте полную ссылку на профиль пользователя)",
        )
        return

    service = await get_user_settings_service()

    if tg_id in await service.superadmin_get_current_allowed_user(tg_id):
        await safe_edit_message(message, "❌ Пользователь уже добавлен.")
        await state.set_state(None)
        return

    await service.superadmin_add_allowed_user(tg_id)

    await message.answer(
        f"✅ Пользователь с ID `{tg_id}` добавлен.",
        parse_mode="Markdown",
    )
    await state.set_state(None)


async def handle_delete_user_button(callback: types.CallbackQuery):
    _, _, tg_id_str = callback.data.split("|")
    tg_id = int(tg_id_str)

    service = await get_user_settings_service()
    await service.superadmin_delete_allowed_user(tg_id)

    await callback.answer("✅ Пользователь удалён.")

    users = await service.superadmin_get_all_allowed_users()

    if not users:
        text = "📭 Нет ни одного разрешённого пользователя."
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="➕ Добавить пользователя",
                        callback_data="user_access|add",
                    ),
                ],
            ],
        )
    else:
        text = "👥 Разрешённые пользователи:\nНажмите на пользователя, чтобы удалить."
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=f"🗑 {uid}",
                        callback_data=f"user_access|delete|{uid}",
                    ),
                ]
                for uid in users
            ]
            + [
                [
                    InlineKeyboardButton(
                        text="➕ Добавить пользователя",
                        callback_data="user_access|add",
                    ),
                ],
            ],
        )

    await safe_edit_message(callback.message, text, reply_markup=kb)


async def handle_allowed_users(callback: types.CallbackQuery):
    service = await get_user_settings_service()
    users = await service.superadmin_get_all_allowed_users()

    if not users:
        text = "📭 Нет ни одного разрешённого пользователя."
    else:
        text = "👥 Разрешённые пользователи:\nНажмите на пользователя, чтобы удалить."

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=f"🗑 {uid}",
                    callback_data=f"user_access|delete|{uid}",
                ),
            ]
            for uid in users
        ]
        + [
            [
                InlineKeyboardButton(
                    text="➕ Добавить пользователя",
                    callback_data="user_access|add",
                ),
            ],
        ],
    )

    await safe_edit_message(callback.message, text, reply_markup=kb)


def hand_add():
    router.callback_query.register(
        handle_model_menu,
        lambda call: call.data == "super_admin|model_settings",
    )
    router.callback_query.register(
        handle_model_setting_selected,
        lambda call: call.data.startswith("super_admin|select_model_setting|"),
    )
    router.callback_query.register(
        handle_add_model,
        lambda call: call.data.startswith("super_admin|add_model|"),
    )
    router.message.register(
        process_add_model_name,
        StateFilter(ModelEditStates.waiting_for_model_name),
    )
    router.callback_query.register(
        handle_edit_model,
        lambda call: call.data.startswith("super_admin|edit_model|"),
    )
    router.message.register(
        process_model_rename,
        StateFilter(ModelEditStates.waiting_for_model_rename),
    )
    router.callback_query.register(
        handle_delete_model,
        lambda call: call.data.startswith("super_admin|delete_model|"),
    )
    router.callback_query.register(
        handle_lora_menu,
        lambda call: call.data == "super_admin|lora_settings",
    )
    router.callback_query.register(
        handle_select_setting,
        lambda call: call.data.startswith("super_admin|select_setting|"),
    )
    router.callback_query.register(
        handle_add_lora,
        lambda call: call.data.startswith("super_admin|add_lora|"),
    )
    router.callback_query.register(
        handle_lora_selected,
        lambda call: call.data.startswith("super_admin|select_lora|"),
    )
    router.callback_query.register(
        handle_lora_delete,
        lambda call: call.data.startswith("super_admin|delete_lora|"),
    )
    router.callback_query.register(
        handle_lora_edit,
        lambda call: call.data.startswith("super_admin|edit_lora|"),
    )
    router.message.register(
        process_lora_title_edit,
        StateFilter(LoraEditStates.waiting_for_new_title),
    )
    router.message.register(
        process_lora_add,
        StateFilter(LoraEditStates.waiting_for_add_title),
    )
    router.callback_query.register(
        handle_add_user,
        lambda call: call.data.startswith("user_access|add"),
    )
    router.message.register(
        process_add_user,
        StateFilter(UserAccessStates.waiting_for_add_user),
    )
    router.callback_query.register(
        handle_delete_user_button,
        lambda call: call.data.startswith("user_access|delete|"),
    )
    router.callback_query.register(
        handle_allowed_users,
        lambda call: call.data.startswith("super_admin|allowed_users"),
    )
