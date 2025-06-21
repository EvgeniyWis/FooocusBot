from bot.utils.googleDrive.auth import service


# Функция для получения данных папки по её id
def getFolderDataByID(folder_id: str):
    try:
        folder = (
            service.files()
            .get(
                fileId=folder_id,
                fields="webViewLink, parents, id",
            )
            .execute()
        )
        return folder
    except Exception as e:
        raise Exception(f"Произошла ошибка при получении данных папки: {e}")
