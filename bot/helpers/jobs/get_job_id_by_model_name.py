from aiogram.fsm.context import FSMContext


async def get_job_id_by_model_name(state: FSMContext, model_name: str, model_key: str = None) -> str:
    """
    Возвращает job_id по model_name из state (job_id_to_full_model_key).
    Если передан model_key, ищет точное совпадение.
    Если не найдено — выбрасывает Exception.
    
    Args:
        state: FSMContext - контекст состояния
        model_name: str - имя модели
        model_key: str - уникальный ключ модели (например, "1", "1+1") для точного поиска
    """
    state_data = await state.get_data()
    job_map = state_data.get("job_id_to_full_model_key", {})
    
    if model_key:
        # Ищем точное совпадение с полным ключом
        full_key = f"{model_name}_{model_key}"
        for k, v in job_map.items():
            if v == full_key:
                return k
        # Если точного совпадения нет, пробуем по префиксу (на случай ключей вида "4+1", когда пришёл только "4")
        for k, v in job_map.items():
            if v.startswith(full_key):
                return k
        raise Exception(f"Не найден job_id для model_name={model_name} с ключом={model_key}")
    else:
        # Обратная совместимость - ищем по началу имени модели
        for k, v in job_map.items():
            if v == model_name:
                return k
        for k, v in job_map.items():
            if v.startswith(f"{model_name}_"):
                return k
        raise Exception(f"Не найден job_id для model_name={model_name}")
