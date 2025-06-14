from bot.utils.generateImages.dataArray.getModelNameIndex import (
    getModelNameIndex,
)
from bot.utils.googleDrive.auth import service


async def getAllFolders(model_names: list[str] = None):
    """
    Получает отформатированный список папок в Google Drive с основными ссылками на папки моделей
    Args:
        model_names (list[str], optional): Список моделей, для которых нужно получить папки.
            Если не указан, будут получены все папки на диске.
    Returns:
        str: Отформатированный текст со списком моделей и ссылками на их папки
    """
    try:
        # Создаем query для поиска только папок
        query = "mimeType='application/vnd.google-apps.folder'"

        # Словарь для хранения информации по моделям
        models_info = {}
        # Словарь для хранения дат создания папок
        folder_dates = {}
        page_token = None

        while True:
            response = (
                service.files()
                .list(
                    q=query,
                    spaces="drive",
                    fields="nextPageToken, files(id, name, webViewLink, createdTime)",
                    pageToken=page_token,
                    supportsAllDrives=True,
                    includeItemsFromAllDrives=True,
                )
                .execute()
            )

            for folder in response.get("files", []):
                folder_name = folder.get("name")
                if folder_name not in ["video", "picture", "2025-06-03"] and (
                    model_names is None or folder_name in model_names
                ):
                    model_name = folder.get("name")
                    created_time = folder.get("createdTime")

                    # Проверяем, существует ли уже папка с таким именем
                    if model_name in folder_dates:
                        # Если новая папка создана позже, обновляем информацию
                        if created_time > folder_dates[model_name]:
                            folder_dates[model_name] = created_time
                            models_info[model_name] = folder.get("webViewLink")
                    else:
                        # Если папка с таким именем встречается впервые
                        folder_dates[model_name] = created_time
                        models_info[model_name] = folder.get("webViewLink")

            page_token = response.get("nextPageToken")
            if not page_token:
                break

        # Создаем список кортежей (индекс, имя, ссылка) для сортировки
        model_data = []
        for model_name, link in models_info.items():
            model_index = getModelNameIndex(model_name)
            if model_index:
                model_data.append((model_index, model_name, link))

        # Сортируем по индексу и формируем вывод
        formatted_output = []
        for model_index, model_name, link in sorted(model_data):
            formatted_output.append(
                f"👱‍♀️ ({model_index}) Модель: {model_name}\n📁 Папка: {link}"
            )

        return "\n\n".join(formatted_output)

    except Exception as e:
        raise Exception(f"Произошла ошибка при получении списка папок: {e}")
