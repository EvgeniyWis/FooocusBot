from functools import wraps

from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
)
from states.StartGenerationState import UserLoraEditStates, UserPromptWrite
from utils.handlers.messages import safe_edit_message

from bot.factory.user_factory import get_user_settings_service
from bot.InstanceBot import router
from bot.keyboards import users_keyboards


def is_registered(func):
    @wraps(func)
    async def wrapper(callback: CallbackQuery, *args, **kwargs):
        service = await get_user_settings_service()
        user_db_id = await service.repo.get_user_db_id(callback.from_user.id)
        if user_db_id is not None:
            return await func(callback, *args, **kwargs)
        else:
            return await safe_edit_message(
                callback.message,
                "⚠️ Вы не зарегистрированы.\n\nНажмите на кнопку ниже, чтобы зарегистрироваться.",
                reply_markup=users_keyboards.user_registration_keyboard(),
            )

    return wrapper


async def show_user_profile(callback: CallbackQuery):
    message = callback.message
    user_id = callback.from_user.id
    service = await get_user_settings_service()

    user_db_id = await service.repo.get_user_db_id(user_id)
    if user_db_id is None:
        await safe_edit_message(
            callback.message,
            "⚠️ У вас ещё не создан профиль.\n\nНажмите на кнопку ниже, чтобы создать его.",
            reply_markup=users_keyboards.user_registration_keyboard(),
        )
        return

    stats = {}
    for setting_number in range(1, 5):
        user_loras = await service.user_get_loras_by_setting(
            user_db_id,
            setting_number,
        )
        # user_prompts = await service.user_get_prompts_by_setting(user_db_id, setting_number)
        user_prompts = [1, 2, 3]
        if user_loras or user_prompts:
            stats[setting_number] = {
                "loras": len(user_loras),
                "prompts": len(user_prompts),
            }

    if not stats:
        text = "⚠️ У вас пока нет сохранённых LoRA и промтов."
    else:
        text = "👤 *Ваш профиль*\n\n⚙️ *Настройки с вашими данными:*\n\n"
        for sn, counts in sorted(stats.items()):
            text += f"• Настройка {sn}: {counts['loras']} LoRA, {counts['prompts']} промт{'ов' if counts['prompts'] != 1 else ''}\n"

        text += "\nДля управления LoRA и промтами выберите настройку в меню «LoRA настройки»."

    await safe_edit_message(
        message,
        text,
        parse_mode="Markdown",
        reply_markup=users_keyboards.user_lora_setting_selector_keyboard(),
    )


async def create_user_profile(call: CallbackQuery):
    user_id = call.from_user.id
    service = await get_user_settings_service()

    await service.ensure_user_exists(user_id)
    await safe_edit_message(
        call.message,
        "✅ Профиль успешно создан. Теперь вы можете использовать все функции настроек!",
    )


@is_registered
async def user_handle_lora_menu(callback: CallbackQuery):
    keyboard = users_keyboards.user_lora_setting_selector_keyboard()
    await safe_edit_message(
        callback.message,
        "⚙️ Выберите настройку:",
        reply_markup=keyboard,
    )


async def show_user_loras_for_setting(
    callback: CallbackQuery,
    state: FSMContext,
    setting_number: int,
):
    await state.update_data(setting_number=setting_number)

    service = await get_user_settings_service()
    user_id_db = await service.repo.get_user_db_id(callback.from_user.id)
    user_loras = await service.user_get_loras_by_setting(
        user_id_db,
        setting_number,
    )
    await service.superadmin_get_all_loras(setting_number)

    # Собираем model_id -> model_name
    model_map = {
        model["id"]: model["name"]
        for model in await service.repo.superadmin_get_models_by_setting(
            setting_number,
        )
    }

    if user_loras:
        text = f"📋 Ваши LoRA для настройки {setting_number}:\n"
        for l in user_loras:
            model_name = model_map.get(l["model_id"], "❓Unknown")
            text += f"• LoRA ID: {l['lora_id']}, Модель: {model_name}, Вес: {l['weight']}\n"
    else:
        text = f"⚠️ У вас пока нет LoRA для настройки {setting_number}."

    keyboard = users_keyboards.show_user_loras_keyboard(
        model_map,
        user_loras,
        setting_number,
    )
    await safe_edit_message(callback.message, text, reply_markup=keyboard)


@is_registered
async def user_handle_select_setting(
    callback: CallbackQuery,
    state: FSMContext,
):
    try:
        _, _, setting_str = callback.data.split("|", 2)
        setting_number = int(setting_str)
    except ValueError:
        await callback.answer("❌ Ошибка: неверный формат callback_data.")
        return

    await show_user_loras_for_setting(callback, state, setting_number)


@is_registered
async def user_handle_add_lora(callback: CallbackQuery, state: FSMContext):
    _, _, setting_str = callback.data.split("|")
    setting_number = int(setting_str)

    service = await get_user_settings_service()
    superadmin_loras = await service.superadmin_get_all_loras(setting_number)
    titles = [l["title"] for l in superadmin_loras]

    await state.update_data(setting_number=setting_number)
    await safe_edit_message(
        callback.message,
        "Выберите LoRA для добавления:",
        reply_markup=users_keyboards.select_lora_keyboard(
            titles,
            setting_number,
        ),
    )


@is_registered
async def user_handle_add_lora_confirm(
    callback: CallbackQuery,
    state: FSMContext,
):
    try:
        _, _, setting_str, title = callback.data.split("|", 3)
        setting_number = int(setting_str)
    except ValueError:
        await callback.answer("❌ Ошибка: неверный формат callback_data.")
        return

    service = await get_user_settings_service()
    lora_id = await service.superadmin_get_lora_id(title, setting_number)
    if lora_id is None:
        await safe_edit_message(
            callback.message,
            "❌ LoRA не найдена в общем списке.",
        )
        return

    await state.update_data(
        selected_lora_id=lora_id,
        setting_number=setting_number,
        selected_lora_title=title,
    )

    models = await service.repo.superadmin_get_models_by_setting(
        setting_number,
    )

    await safe_edit_message(
        callback.message,
        "📦 Выберите модель для этой LoRA:",
        reply_markup=users_keyboards.select_model_for_lora_keyboard(
            models,
            setting_number,
        ),
    )


@is_registered
async def user_handle_select_model_for_lora(
    callback: CallbackQuery,
    state: FSMContext,
):
    _, _, model_id_str = callback.data.split("|")
    model_id = int(model_id_str)

    data = await state.get_data()
    lora_id = data["selected_lora_id"]
    setting_number = data["setting_number"]

    service = await get_user_settings_service()
    user_id = callback.from_user.id
    user_db_id = await service.repo.get_user_db_id(user_id)

    await service.user_add_lora(
        user_db_id,
        lora_id,
        model_id,
        setting_number,
        1.0,
    )

    await safe_edit_message(
        callback.message,
        "✅ LoRA успешно добавлена к выбранной модели с стандартным весом = 1.0.",
    )
    await show_user_loras_for_setting(callback, state, setting_number)


@is_registered
async def user_handle_select_lora(callback: CallbackQuery, state: FSMContext):
    try:
        _, _, setting_str, lora_id_str, model_id_str = callback.data.split("|")
        setting_number = int(setting_str)
        lora_id = int(lora_id_str)
        model_id = int(model_id_str)
    except Exception:
        await callback.answer("❌ Ошибка: неверный формат callback_data.")
        return

    await state.update_data(
        setting_number=setting_number,
        selected_lora_id=lora_id,
        selected_model_id=model_id,
    )

    await safe_edit_message(
        callback.message,
        f"Настройки для LoRA ID {lora_id} (Модель ID {model_id}):",
        reply_markup=users_keyboards.lora_user_menu_keyboard(setting_number),
    )


@is_registered
async def user_handle_edit_lora_weight(
    callback: CallbackQuery,
    state: FSMContext,
):
    await safe_edit_message(
        callback.message,
        "Введите новый вес для LoRA (например, +0.5 или -0.5 (по умолчанию вес прибавляется)):",
    )
    await state.set_state(UserLoraEditStates.waiting_for_weight_input)


@is_registered
async def user_handle_weight_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lora_id = data.get("selected_lora_id")
    model_id = data.get("selected_model_id")
    setting_number = data.get("setting_number")
    user_id = message.from_user.id

    service = await get_user_settings_service()
    user_db_id = await service.repo.get_user_db_id(user_id)

    # Получаем текущий вес
    current_weight = await service.repo.user_get_lora_weight(
        user_db_id,
        lora_id,
        model_id,
        setting_number,
    )

    try:
        delta_weight = float(message.text)
        if delta_weight < -10 or delta_weight > 10:
            raise ValueError()
    except ValueError:
        await message.answer(
            "❌ Некорректное значение веса. Введите число от -10 до 10.",
        )
        return

    new_weight = await service.user_update_lora_weight_delta(
        user_db_id,
        lora_id,
        model_id,
        setting_number,
        delta_weight,
    )

    await message.answer(
        f"✅ Вес LoRA обновлён: {current_weight:.2f} {'+' if delta_weight >= 0 else ''}{delta_weight:.2f} = {new_weight:.2f}",
    )
    await state.clear()


@is_registered
async def user_handle_delete_lora(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lora_id = data.get("selected_lora_id")
    model_id = data.get("selected_model_id")
    setting_number = data.get("setting_number")
    user_id = callback.from_user.id

    service = await get_user_settings_service()
    user_db_id = await service.repo.get_user_db_id(user_id)

    await service.user_delete_lora(
        user_db_id,
        lora_id,
        model_id,
        setting_number,
    )

    await safe_edit_message(callback.message, "✅ LoRA успешно удалена.")
    await show_user_loras_for_setting(callback, state, setting_number)


@is_registered
async def user_handle_add_prompt(callback: CallbackQuery):
    await safe_edit_message(
        callback.message,
        "Выберите тип промпта:",
        reply_markup=users_keyboards.prompt_type_selector_keyboard(),
    )


@is_registered
async def user_handle_prompt_type_selection(
    callback: CallbackQuery,
    state: FSMContext,
):
    _, _, _, prompt_type = callback.data.split("|")

    await state.update_data(prompt_type=prompt_type)

    await safe_edit_message(
        callback.message,
        "⚙️ Выберите настройку:",
        reply_markup=users_keyboards.prompt_admin_setting_selector_keyboard(),
    )


@is_registered
async def user_handle_select_settings_for_prompt(
    callback: CallbackQuery,
    state: FSMContext,
):
    _, _, _, setting_str = callback.data.split("|")
    setting_number = int(setting_str)

    service = await get_user_settings_service()
    models = await service.repo.superadmin_get_models_by_setting(
        setting_number,
    )

    await state.update_data(setting_number=setting_number)

    await safe_edit_message(
        callback.message,
        "📦 Выберите модель:",
        reply_markup=users_keyboards.select_model_for_prompt_keyboard(
            models,
        ),
    )


@is_registered
async def user_handle_select_model_for_prompt(
    callback: CallbackQuery,
    state: FSMContext,
):
    _, _, model_id_str = callback.data.split("|")
    model_id = int(model_id_str)

    data = await state.get_data()
    setting_number = data["setting_number"]
    prompt_type = data["prompt_type"]
    user_id = callback.from_user.id

    await state.update_data(selected_model_id=model_id)

    service = await get_user_settings_service()
    user_db_id = await service.repo.get_user_db_id(user_id)

    prompt = await service.user_get_prompt(
        user_db_id,
        model_id,
        setting_number,
        prompt_type=prompt_type,
    )

    if prompt:
        text = f"📄 *Ваш {prompt_type} промпт:*\n\n`{prompt}`"
        keyboard = users_keyboards.prompt_manage_keyboard(prompt_exists=True)
    else:
        text = f"❌ {prompt_type.capitalize()} промпт пока не задан."
        keyboard = users_keyboards.prompt_manage_keyboard(prompt_exists=False)

    await safe_edit_message(
        callback.message,
        text,
        reply_markup=keyboard,
        parse_mode="Markdown",
    )


@is_registered
async def user_handle_prompt_edit(callback: CallbackQuery, state: FSMContext):
    await safe_edit_message(
        callback.message,
        "✏️ Введите текст промпта:",
    )
    await state.set_state(UserPromptWrite.waiting_for_prompt_input)


async def user_handle_prompt_input(message: types.Message, state: FSMContext):
    data = await state.get_data()
    setting_number = data["setting_number"]
    model_id = data["selected_model_id"]
    prompt_type = data["prompt_type"]
    user_id = message.from_user.id

    service = await get_user_settings_service()
    user_db_id = await service.repo.get_user_db_id(user_id)

    prompt_text = message.text.strip()
    await service.user_add_prompt(
        user_db_id,
        model_id,
        setting_number,
        prompt_text,
        prompt_type=prompt_type,
    )

    await message.answer("✅ Промпт успешно сохранён.")
    await state.clear()


@is_registered
async def user_handle_prompt_delete(
    callback: CallbackQuery,
    state: FSMContext,
):
    data = await state.get_data()
    setting_number = data["setting_number"]
    model_id = data["selected_model_id"]
    prompt_type = data["prompt_type"]
    user_id = callback.from_user.id

    service = await get_user_settings_service()
    user_db_id = await service.repo.get_user_db_id(user_id)

    await service.user_delete_prompt(
        user_db_id,
        model_id,
        setting_number,
        prompt_type=prompt_type,
    )

    await safe_edit_message(
        callback.message,
        f"✅ {prompt_type.capitalize()} промпт удалён.",
    )


async def back_to_settings(callback: CallbackQuery):
    await safe_edit_message(
        callback.message,
        "⚙️ Выберите настройку:",
        reply_markup=users_keyboards.prompt_admin_setting_selector_keyboard(),
    )


async def back_to_models(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    setting_number = data["setting_number"]

    service = await get_user_settings_service()
    models = await service.repo.superadmin_get_models_by_setting(
        setting_number,
    )

    await safe_edit_message(
        callback.message,
        "📦 Выберите модель:",
        reply_markup=users_keyboards.select_model_for_prompt_keyboard(models),
    )


async def back_to_type(callback: CallbackQuery):
    await safe_edit_message(
        callback.message,
        "Выберите тип промпта:",
        reply_markup=users_keyboards.prompt_type_selector_keyboard(),
    )


def hand_add():
    router.callback_query.register(
        show_user_profile,
        lambda call: call.data.startswith("user|profile"),
    )
    router.callback_query.register(
        create_user_profile,
        lambda call: call.data.startswith("user|create_profile"),
    )
    router.callback_query.register(
        user_handle_delete_lora,
        lambda call: call.data.startswith("user|delete_lora"),
    )
    router.message.register(
        user_handle_weight_input,
        StateFilter(UserLoraEditStates.waiting_for_weight_input),
    )

    router.callback_query.register(
        user_handle_select_lora,
        lambda c: c.data.startswith("user|select_lora|"),
    )
    (
        router.callback_query.register(
            user_handle_select_model_for_lora,
            lambda c: c.data.startswith("user|select_model_for_lora|"),
        ),
    )
    router.callback_query.register(
        user_handle_add_lora_confirm,
        lambda c: c.data.startswith("user|add_lora_confirm|"),
    )
    router.callback_query.register(
        user_handle_add_lora,
        lambda c: c.data.startswith("user|add_lora|"),
    )
    router.callback_query.register(
        user_handle_select_setting,
        lambda c: c.data.startswith("user|select_setting|"),
    )
    router.callback_query.register(
        user_handle_lora_menu,
        lambda c: c.data.startswith("user|lora_settings"),
    )
    router.callback_query.register(
        user_handle_edit_lora_weight,
        lambda c: c.data.startswith("user|edit_lora_weight"),
    )
    router.callback_query.register(
        user_handle_add_prompt,
        lambda c: c.data == "user|prompts",
    )
    router.callback_query.register(
        user_handle_select_settings_for_prompt,
        lambda c: c.data.startswith("user|prompt|select_setting|"),
    )
    router.callback_query.register(
        user_handle_select_model_for_prompt,
        lambda c: c.data.startswith("user|select_model_for_prompt|"),
    )
    router.callback_query.register(
        user_handle_prompt_edit,
        lambda c: c.data == "user|prompt|edit",
    )
    router.callback_query.register(
        user_handle_prompt_delete,
        lambda c: c.data == "user|prompt|delete",
    )
    router.message.register(
        user_handle_prompt_input,
        StateFilter(UserPromptWrite.waiting_for_prompt_input),
    )
    router.callback_query.register(
        user_handle_prompt_type_selection,
        lambda c: c.data.startswith("user|prompt|type|"),
    )
    router.callback_query.register(
        back_to_settings,
        lambda c: c.data == "user|prompt|back_to_settings",
    )
    router.callback_query.register(
        back_to_settings,
        lambda c: c.data == "user|prompt|back_to_settings",
    )
    router.callback_query.register(
        back_to_models,
        lambda c: c.data == "user|prompt|back_to_models",
    )
    router.callback_query.register(
        back_to_type,
        lambda c: c.data == "user|prompt|back_to_type",
    )
