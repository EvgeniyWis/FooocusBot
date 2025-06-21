# Функция для конвертации ссылки Google Drive в прямую ссылку для скачивания
def convertDriveLink(url: str) -> str:
    """Конвертирует ссылку Google Drive в прямую ссылку для скачивания."""
    if "drive.google.com" not in url:
        return url

    file_id = url.split("/d/")[1].split("/")[0]
    return f"https://drive.google.com/uc?export=view&id={file_id}"
