from factory.user_factory import get_user_settings_service
from helpers.generateImages.dataArray.get_final_loras_for_user import (
    get_final_loras_for_model,
)

from bot.helpers.generateImages.dataArray.generate_data import generate_data
from bot.helpers.generateImages.dataArray.setting_1.generate_loras import (
    setting1_generate_loras,
)
from bot.settings import settings


# Функция для генерации данных для запроса настройки 1
async def setting1_generate_data(
    user_id: int,
    model_name: str,
    picture_folder_id: str,
    video_folder_id: str,
    prompt: str,
    loras_weights: list[int] | None,
    image_number: int = 4,
    negative_prompt: str = settings.COMMON_NEGATIVE_PROMPT,
    default_data_array: list[dict] | None = None,
):
    settings_service = await get_user_settings_service()
    user_id_db = await settings_service.repo.get_user_by_user_id(user_id)
    model_id = await settings_service.repo.get_model_id(model_name, 1)
    loras = await get_final_loras_for_model(user_id_db, 1, model_id)

    if len(loras) == 0:
        # 👇 Попробуем вытащить веса из default_data_array
        if loras_weights is None and default_data_array is not None:
            weights = _extract_weights_from_default_array(
                default_data_array,
                model_name,
            )
            if weights is not None:
                loras_weights = weights

        if loras_weights is None:
            raise ValueError(
                f"Lora weights are required for model={model_name} when no user loras",
            )

        loras = setting1_generate_loras(loras_weights)

    base_config_model_name = "CyberRealistic_Pony.safetensors"
    data = generate_data(
        model_name,
        picture_folder_id,
        video_folder_id,
        prompt,
        loras,
        base_config_model_name,
        image_number,
        negative_prompt,
    )
    return data


def _extract_weights_from_default_array(
    default_data_array: list[dict],
    model_name: str,
) -> list[float] | None:
    for item in default_data_array:
        if item["model_name"] == model_name:
            try:
                loras = item["json"]["input"]["loras"]
                return [l["weight"] for l in loras]
            except (KeyError, TypeError):
                return None
    return None
