from bot.factory.user_factory import get_user_settings_service


async def get_final_loras_for_user(
    user_id: int,
    setting_number: int,
) -> list[dict]:
    settings_service = await get_user_settings_service()
    rows = await settings_service.user_get_loras_by_setting(
        user_id,
        setting_number,
    )

    if not rows:
        return []

    loras = []
    for row in rows:
        try:
            # Пытаемся получить атрибуты как у объекта
            weight = getattr(row, "weight", None)
            model_name = getattr(row, "model_name", None)

            # Или как у словаря, если это не сработает
            if weight is None and hasattr(row, "__getitem__"):
                weight = row.get("weight")
                model_name = row.get("model_name")

            if model_name is not None and weight is not None:
                loras.append(
                    {
                        "name": str(model_name).strip(),
                        "weight": float(weight),
                    },
                )
        except (ValueError, AttributeError, TypeError) as e:
            logger.error(f"Ошибка при обработке строки лоры: {e}, row: {row}")
            continue

    return loras
