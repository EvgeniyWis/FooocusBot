from aiogram.fsm.context import FSMContext


async def get_job_id_by_model_name(state: FSMContext, model_name: str, model_key: str = None) -> str:
    """
    Возвращает job_id по model_name из state (job_id_to_full_model_key).
    Если передан model_key, ищет точное совпадение.
    Если не найдено — выбрасывает Exception.
    
    Поведение обновлено: при наличии нескольких job_id для одной модели
    возвращается самый свежий (последний добавленный) job_id.
    
    Args:
        state: FSMContext - контекст состояния
        model_name: str - имя модели
        model_key: str - уникальный ключ модели (например, "1", "1+1") для точного поиска
    """
    state_data = await state.get_data()
    job_map = state_data.get("job_id_to_full_model_key", {})

    # Преобразуем items в список и обходим в обратном порядке вставки,
    # чтобы вернуть самый свежий job_id
    items_reversed = list(job_map.items())[::-1]

    if model_key:
        full_key = f"{model_name}_{model_key}"
        # Сначала — точное совпадение
        for k, v in items_reversed:
            if v == full_key:
                return k
        # Затем — по префиксу (например, ключи вида "4+1" при переданном "4")
        for k, v in items_reversed:
            if v.startswith(full_key):
                return k
        raise Exception(f"Не найден job_id для model_name={model_name} с ключом={model_key}")
    else:
        # Обратная совместимость — без model_key
        for k, v in items_reversed:
            if v == model_name:
                return k
        for k, v in items_reversed:
            if v.startswith(f"{model_name}_"):
                return k
        raise Exception(f"Не найден job_id для model_name={model_name}")
