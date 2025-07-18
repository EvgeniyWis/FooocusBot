from logger import logger

from bot.factory.user_factory import get_user_settings_service


async def get_final_loras_for_model(
    user_id: int,
    setting_number: int,
    model_id: int,
) -> list[dict]:
    settings_service = await get_user_settings_service()

    all_loras = await settings_service.user_get_loras_by_setting(
        user_id,
        setting_number,
    )

    # Разделим на override и базовые
    override_loras = []
    base_loras = []

    for row in all_loras:
        lora_model_id = row.get("model_id")
        is_override = row.get("is_override", False)

        if is_override and lora_model_id == model_id:
            override_loras.append(row)
        elif lora_model_id is None:
            base_loras.append(row)

    selected_loras = override_loras if override_loras else base_loras

    result = []
    for lora in selected_loras:
        try:
            weight = lora.get("weight")
            model_name = lora.get("model_name")
            name = str(model_name).strip() if model_name else None
            if name:
                result.append(
                    {
                        "name": name,
                        "weight": float(weight),
                    }
                )
        except Exception as e:
            logger.error(f"Ошибка при обработке лоры: {e} — {lora}")
            continue

    return result
