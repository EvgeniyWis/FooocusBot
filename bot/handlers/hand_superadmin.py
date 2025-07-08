from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.startGeneration.keyboards import (
    lora_admin_menu_keyboard,
    lora_list_keyboard,
    selected_lora_action_keyboard,
)
from utils.handlers.messages import safe_edit_message

from bot.factory.user_factory import get_user_settings_service
from bot.InstanceBot import router


class LoraEditStates(StatesGroup):
    waiting_for_new_title = State()
    waiting_for_add_title = State()


async def handle_lora_menu(callback: types.CallbackQuery):
    await safe_edit_message(
        callback.message,
        "⚙️ Управление LoRA:",
        reply_markup=lora_admin_menu_keyboard(),
    )


async def handle_show_loras(callback: types.CallbackQuery):
    service = await get_user_settings_service()
    loras = await service.get_all_loras()
    lora_titles = [l["title"] for l in loras]

    if not lora_titles:
        await safe_edit_message(
            callback.message,
            "❌ LoRA моделей нет в базе.",
        )
        return

    await safe_edit_message(
        callback.message,
        "📋 Список LoRA моделей:\nНажмите, чтобы выбрать.",
        reply_markup=lora_list_keyboard(lora_titles),
    )


async def handle_lora_selected(callback: types.CallbackQuery):
    _, _, title = callback.data.split("|", 2)
    await safe_edit_message(
        callback.message,
        f"📌 Вы выбрали LoRA: *{title}*",
        parse_mode="Markdown",
        reply_markup=selected_lora_action_keyboard(title),
    )


async def handle_lora_delete(callback: types.CallbackQuery):
    _, _, title = callback.data.split("|", 2)
    service = await get_user_settings_service()
    await service.delete_lora(title)
    await safe_edit_message(
        callback.message,
        f"🗑 LoRA `{title}` удалена.",
        parse_mode="Markdown",
    )
    await handle_show_loras(callback)


async def handle_lora_edit(callback: types.CallbackQuery, state: FSMContext):
    _, _, title = callback.data.split("|", 2)
    await state.set_state(LoraEditStates.waiting_for_new_title)
    await state.update_data(old_title=title)
    await safe_edit_message(
        callback.message,
        f"✏️ Введите новое название для LoRA `{title}`:",
        parse_mode="Markdown",
    )


async def process_lora_title_edit(message: types.Message, state: FSMContext):
    data = await state.get_data()
    old_title = data["old_title"]
    new_title = message.text.strip()

    if not new_title:
        await message.answer(
            "❌ Название не может быть пустым. Повторите попытку.",
        )
        return

    service = await get_user_settings_service()
    await service.delete_lora(old_title)
    await service.add_lora(new_title)

    await message.answer(
        f"✅ LoRA `{old_title}` переименована в `{new_title}`.",
        parse_mode="Markdown",
    )
    await state.clear()


async def handle_add_lora(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(LoraEditStates.waiting_for_add_title)
    await safe_edit_message(
        callback.message,
        "➕ Введите название новой LoRA:",
    )


async def process_lora_add(message: types.Message, state: FSMContext):
    new_title = message.text.strip()
    if not new_title:
        await message.answer(
            "❌ Название не может быть пустым. Повторите попытку.",
        )
        return

    service = await get_user_settings_service()
    await service.add_lora(new_title)

    await message.answer(
        f"✅ LoRA `{new_title}` добавлена в базу.",
        parse_mode="Markdown",
    )
    await state.clear()


def hand_add():
    router.callback_query.register(
        handle_lora_menu,
        lambda c: c.data == "super_admin|lora_settings",
    )
    router.callback_query.register(
        handle_show_loras,
        lambda c: c.data == "super_admin|show_loras",
    )
    router.callback_query.register(
        handle_lora_selected,
        lambda c: c.data.startswith("super_admin|select_lora|"),
    )
    router.callback_query.register(
        handle_lora_delete,
        lambda c: c.data.startswith("super_admin|delete_lora|"),
    )
    router.callback_query.register(
        handle_lora_edit,
        lambda c: c.data.startswith("super_admin|edit_lora|"),
    )
    router.callback_query.register(
        handle_add_lora,
        lambda c: c.data == "super_admin|add_lora",
    )

    router.message.register(
        process_lora_title_edit,
        LoraEditStates.waiting_for_new_title,
    )
    router.message.register(
        process_lora_add,
        LoraEditStates.waiting_for_add_title,
    )
