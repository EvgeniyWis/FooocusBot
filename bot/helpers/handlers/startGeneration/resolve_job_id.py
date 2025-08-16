from typing import Any, Dict, Optional

from bot.app.core.logging import logger


def resolve_job_id(
    state_data: Dict[str, Any],
    model_name: str,
    model_key: Optional[str],
    message_id: Optional[int],
    short_job_id: Optional[str],
) -> Optional[str]:
    """Определяет полный job_id по данным состояния и контексту нажатия.

    Порядок поиска:
    1) По префиксу short_job_id среди job_id в медиагруппе/клавиатурах
    2) По записи клавиатуры с совпадающим message_id
    3) По записи клавиатуры с совпадающим model_name (и опционально префикс)
    4) По маппингу state_data['job_id_to_full_model_key'] и полному ключу модели
    5) По словарю state_data['jobs'] c префиксом short_job_id и проверкой маппинга модели
    """
    mediagroup_data = state_data.get("imageGeneration_mediagroup_messages_ids", []) or []

    job_id: Optional[str] = None

    # 1) Поиск по префиксу short_job_id среди возможных job_id из медиагруппы
    if short_job_id:
        possible_job_ids = [item.get("job_id") for item in mediagroup_data if item.get("job_id")]
        possible_job_ids = list({jid for jid in possible_job_ids if isinstance(jid, str)})
        for jid in possible_job_ids:
            if jid.startswith(short_job_id):
                job_id = jid
                break

    # 2) Поиск записи клавиатуры по текущему message_id
    if not job_id and message_id is not None:
        for item in mediagroup_data:
            if (
                item.get("type") == "keyboard"
                and item.get("message_id") == message_id
            ):
                job_id = item.get("job_id")
                break

    # 3) Любая запись клавиатуры для этой модели
    if not job_id:
        for item in mediagroup_data:
            if item.get("type") == "keyboard" and item.get("model_name") == model_name:
                candidate = item.get("job_id")
                if not short_job_id or (isinstance(candidate, str) and candidate.startswith(short_job_id)):
                    job_id = candidate
                    break

    # 4) По словарю соответствий job_id -> full_model_key
    if not job_id:
        try:
            mapping = state_data.get("job_id_to_full_model_key", {}) or {}
            target_full_key = f"{model_name}/{model_key}" if model_key is not None else model_name
            candidates = []
            if short_job_id:
                candidates = [
                    jid for jid, full_key in mapping.items()
                    if isinstance(jid, str) and jid.startswith(short_job_id) and full_key == target_full_key
                ]
            if not candidates:
                candidates = [jid for jid, full_key in mapping.items() if full_key == target_full_key]
            if candidates:
                job_id = candidates[0]
        except Exception as e:
            logger.warning(f"[resolve_job_id] Mapping lookup failed: {e}")

    # 5) По словарю jobs с проверкой маппинга модели
    if not job_id and short_job_id:
        try:
            jobs_dict = state_data.get("jobs", {}) or {}
            mapping = state_data.get("job_id_to_full_model_key", {}) or {}
            target_full_key = f"{model_name}/{model_key}" if model_key is not None else model_name
            for jid in jobs_dict.keys():
                if isinstance(jid, str) and jid.startswith(short_job_id):
                    if not mapping or mapping.get(jid) == target_full_key:
                        job_id = jid
                        break
        except Exception as e:
            logger.warning(f"[resolve_job_id] Jobs dict lookup failed: {e}")

    return job_id 