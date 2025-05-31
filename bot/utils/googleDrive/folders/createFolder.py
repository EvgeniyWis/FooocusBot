from ..auth import service


# Создание папки
async def createFolder(folder_name: str, nested_folder_names: list[str] = None, parent_folder_id: str = None) -> tuple[str, str]:
    # Создание метаданных для новой папки
    folder_metadata = {
        "name": folder_name,  # Имя вашей папки
        "mimeType": "application/vnd.google-apps.folder",
    }

    if parent_folder_id:
        folder_metadata["parents"] = [parent_folder_id]

    # Создание папки
    folder = service.files().create(
        body=folder_metadata,
        fields="id,webViewLink",
        supportsAllDrives=True,
    ).execute()

    # Установка публичного доступа
    permission = {
        "type": "anyone",
        "role": "reader",
        "allowFileDiscovery": True,
    }
    service.permissions().create(
        fileId=folder.get("id"),
        body=permission,
        fields="id",
        supportsAllDrives=True,
    ).execute()

    if nested_folder_names:
        nested_folders_array = []

        for nested_folder_name in nested_folder_names:
            # Создание вложенной папки
            nested_folder_metadata = {
                "name": nested_folder_name,
                "mimeType": "application/vnd.google-apps.folder",
                "parents": [folder["id"]],
            }
            nested_folder = service.files().create(body=nested_folder_metadata, fields="id,webViewLink").execute()

            nested_folders_array.append({
                "id": nested_folder["id"],
                "webViewLink": nested_folder["webViewLink"],
            })

        return nested_folders_array
    else:
        return folder["id"], folder["webViewLink"]
