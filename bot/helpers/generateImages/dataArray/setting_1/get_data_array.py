from factory.user_factory import get_user_settings_service

from bot.helpers.generateImages.dataArray.setting_1.default_setting1_data_array import (
    default_setting1_get_data_array,
)
from bot.helpers.generateImages.dataArray.setting_1.generate_data import (
    setting1_generate_data,
)
from bot.settings import settings

# TODO: доделать логику с лорами, ибо щас не работает корректно override
# TODO:


async def setting1_get_data_array(user_id: int):
    service = await get_user_settings_service()
    setting_number = 1
    user_id_db = await service.repo.get_user_by_user_id(user_id)

    # Все доступные модели (общие)
    models = await service.repo.superadmin_get_models_by_setting(
        setting_number,
    )
    default_data_array = await default_setting1_get_data_array(user_id)

    data_array = []

    for model in models:
        model_id = model["id"]
        model_name = model["name"]

        # Промпты: если не заданы пользователем — берем из дефолта
        user_prompt = await service.user_get_prompt(
            user_id=user_id_db,
            model_id=model_id,
            setting_number=setting_number,
            prompt_type="positive",
        )
        prompt = user_prompt or _get_default_prompt(
            default_data_array,
            model_name,
        )

        user_negative_prompt = await service.user_get_prompt(
            user_id=user_id_db,
            prompt_type="negative",
            model_id=None,
            setting_number=None,
        )
        negative_prompt = (
            user_negative_prompt or settings.COMMON_NEGATIVE_PROMPT
        )

        # Лора-веса подгружаются внутри generate_data (если пользовательские — то они приоритетны)

        # Извлекаем picture/video folder из дефолта (по model_name)
        picture_folder_id = _get_default_picture_folder_id(
            default_data_array,
            model_name,
        )
        video_folder_id = _get_default_video_folder_id(
            default_data_array,
            model_name,
        )

        data = await setting1_generate_data(
            user_id=user_id,
            model_name=model_name,
            picture_folder_id=picture_folder_id,
            video_folder_id=video_folder_id,
            prompt=prompt,
            loras_weights=None,
            image_number=4,
            negative_prompt=negative_prompt,
            default_data_array=default_data_array,
        )

        data_array.append(data)

    if settings.MOCK_IMAGES_MODE:
        data_array = data_array[:1]

    return data_array


def _get_default_prompt(default_array: list[dict], model_name: str) -> str:
    for item in default_array:
        if item["model_name"] == model_name:
            return item["json"]["input"]["prompt"]


def _get_default_picture_folder_id(
    default_array: list[dict],
    model_name: str,
) -> str:
    for item in default_array:
        if item["model_name"] == model_name:
            return item["picture_folder_id"]
    return "unknown_picture_folder"


def _get_default_video_folder_id(
    default_array: list[dict],
    model_name: str,
) -> str:
    for item in default_array:
        if item["model_name"] == model_name:
            return item["video_folder_id"]
    return "unknown_video_folder"


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
