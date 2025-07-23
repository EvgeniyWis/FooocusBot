from aiogoogle import Aiogoogle

from bot.utils.googleDrive.auth import client_creds, user_creds


# Создание папки
async def createFolder(
    folder_name: str,
    nested_folder_names: list[str] = None,
    parent_folder_id: str = None,
) -> tuple[str, str] | list[dict]:
    folder_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_folder_id:
        folder_metadata["parents"] = [parent_folder_id]

    async with Aiogoogle(client_creds=client_creds, user_creds=user_creds) as aiogoogle:
        drive_v3 = await aiogoogle.discover("drive", "v3")

        # Создание папки
        folder = await aiogoogle.as_user(
            drive_v3.files.create(
                json=folder_metadata,
                fields="id,webViewLink",
                supportsAllDrives=True,
            )
        )

        # Установка публичного доступа
        permission = {
            "type": "anyone",
            "role": "reader",
            "allowFileDiscovery": True,
        }
        await aiogoogle.as_user(
            drive_v3.permissions.create(
                fileId=folder["id"],
                json=permission,
                fields="id",
                supportsAllDrives=True,
            )
        )

        if nested_folder_names:
            nested_folders_array = []
            for nested_folder_name in nested_folder_names:
                nested_folder_metadata = {
                    "name": nested_folder_name,
                    "mimeType": "application/vnd.google-apps.folder",
                    "parents": [folder["id"]],
                }
                nested_folder = await aiogoogle.as_user(
                    drive_v3.files.create(
                        json=nested_folder_metadata,
                        fields="id,webViewLink"
                    )
                )
                nested_folders_array.append(
                    {
                        "id": nested_folder["id"],
                        "webViewLink": nested_folder["webViewLink"],
                    }
                )
            return nested_folders_array
        else:
            return folder["id"], folder["webViewLink"]
