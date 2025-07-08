from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from utils.handlers.messages import safe_edit_message

from bot.factory.user_factory import get_user_settings_service
from bot.InstanceBot import router
from bot.logger import logger


async def show_user_profile(callback: CallbackQuery):
    message = callback.message
    user_id = callback.from_user.id
    logger.info(f"Пользователь {user_id} запросил свой профиль")
    service = await get_user_settings_service()

    user_db_id = await service.repo.get_user_db_id(user_id)
    if user_db_id is None:
        await safe_edit_message(
            "⚠️ У вас ещё не создан профиль.\n\nНажмите на кнопку ниже, чтобы создать его.",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [
                        InlineKeyboardButton(
                            text="📝 Создать профиль",
                            callback_data="user|create_profile",
                        ),
                    ],
                ],
            ),
        )
        return

    # Получаем данные
    loras = await service.get_user_loras(user_id)
    prompts = await service.get_user_prompts(user_id)

    loras_text = (
        "\n".join(
            f"📌 Модель: {l['model_name']} | Настройка: {l['setting_number']} | LoRA ID: {l['lora_id']} | Вес: {l['weight']}"
            for l in loras
        )
        if loras
        else "— нет лор"
    )

    prompts_text = (
        "\n".join(
            f"📝 Модель: {p['model_name']} | Настройка: {p['setting_number']}\n{p['prompt']}"
            for p in prompts
        )
        if prompts
        else "— нет промптов"
    )

    await safe_edit_message(
        message,
        f"👤 *Ваш профиль*\n\n"
        f"📊 *Выбранные LoRA:*\n{loras_text}\n\n"
        f"✍️ *Индивидуальные промпты:*\n{prompts_text}",
        parse_mode="Markdown",
    )


async def create_user_profile(call: CallbackQuery):
    user_id = call.from_user.id
    service = await get_user_settings_service()

    await service.ensure_user_exists(user_id)
    await safe_edit_message(
        call.message,
        "✅ Профиль успешно создан. Теперь вы можете использовать все функции!",
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
