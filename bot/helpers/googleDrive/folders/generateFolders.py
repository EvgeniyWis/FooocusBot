from bot.app.core.logging import logger
from bot.utils.googleDrive.folders.createFolder import createFolder


# Функция для генерации папок в Google Drive по именам моделей
async def generateFolders(model_names: list[str], folder_names: list[str]) -> None:
    # Генерируем корневые папки для моделей
    model_folders_ids = []
    for model_name in model_names:
        id, link = await createFolder(model_name)
        logger.info(
            f"Папка для модели {model_name} создана: {id} по ссылке: {link}"
        )
        model_folders_ids.append(id)

    # Создаём словарь с именем модели и id
    model_folders_dict = dict(zip(model_names, model_folders_ids))

    # Генерируем папки в корневых папках моделей
    total_result = []
    for folder_name in folder_names:
        folders = []
        for model_name, model_folder_id in model_folders_dict.items():
            folder = await createFolder(
                folder_name, parent_folder_id=model_folder_id,
            )
            logger.info(
                f'Папка "{folder_name}" для модели {model_name} создана: {folder}'
            )

            folders.append(folder)

        total_result.append(folders)

    # Возвращаем списки папок
    return folders
