from bot.logger import logger
from bot.utils.googleDrive.folders.createFolder import createFolder


# Функция для генерации папок "picture" и "videos" в Google Drive по именам моделей
async def generateFolders(model_names: list[str]) -> None:
    # Генерируем корневые папки для моделей
    model_folders_ids = []
    for model_name in model_names:
        id, link = await createFolder(model_name)
        logger.info(
            f"Папка для модели {model_name} создана: {id} по ссылке: {link}"
        )
        model_folders_ids.append(id)

    # Создаём словарь с именем модели и id
    model_folders_dict = {
        model_name: model_folder_id
        for model_name, model_folder_id in zip(model_names, model_folders_ids)
    }

    # Генерируем папки "picture" и "videos" в корневых папках моделей
    picture_folders = []
    videos_folders = []
    for model_name, model_folder_id in model_folders_dict.items():
        picture_folder = await createFolder(
            "picture", parent_folder_id=model_folder_id
        )
        logger.info(
            f'Папка "picture" для модели {model_name} создана: {picture_folder}'
        )

        videos_folder = await createFolder(
            "videos", parent_folder_id=model_folder_id
        )
        logger.info(
            f'Папка "videos" для модели {model_name} создана: {videos_folder}'
        )

        picture_folders.append(picture_folder)
        videos_folders.append(videos_folder)

    # Возвращаем списки папок "picture" и "videos"
    return picture_folders, videos_folders
