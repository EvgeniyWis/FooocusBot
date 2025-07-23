from aiogoogle import Aiogoogle

from bot.utils.googleDrive.auth import client_creds, user_creds


# Функция для получения данных папки по её id
async def getFolderDataByID(folder_id: str):
    try:
        async with Aiogoogle(client_creds=client_creds, user_creds=user_creds) as aiogoogle:
            drive_v3 = await aiogoogle.discover("drive", "v3")
            folder = await aiogoogle.as_user(
                drive_v3.files.get(
                    fileId=folder_id,
                    fields="webViewLink, parents, id",
                ),
            )
            return folder
    except Exception as e:
        raise Exception(f"Произошла ошибка при получении данных папки: {e}")
