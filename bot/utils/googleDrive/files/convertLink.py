# Функция для конвертации ссылки Google Drive в прямую ссылку для скачивания
def convertDriveLink(url: str) -> str:
    """Конвертирует ссылку Google Drive в прямую ссылку для скачивания."""
    if "drive.google.com" not in url:
        return url

    # Извлекаем file_id из различных форматов ссылок Google Drive
    file_id = None
    
    # Формат: https://drive.google.com/file/d/{file_id}/view
    if "/file/d/" in url:
        file_id = url.split("/file/d/")[1].split("/")[0]
    # Формат: https://drive.google.com/drive/folders/{file_id}
    elif "/drive/folders/" in url:
        file_id = url.split("/drive/folders/")[1].split("/")[0]
    # Формат: https://drive.google.com/open?id={file_id}
    elif "id=" in url:
        file_id = url.split("id=")[1].split("&")[0]
    # Формат: https://drive.google.com/d/{file_id}
    elif "/d/" in url:
        file_id = url.split("/d/")[1].split("/")[0]
    
    if not file_id:
        return url
    
    # Создаем прямую ссылку для скачивания с дополнительными параметрами
    # Используем несколько вариантов для максимальной совместимости
    return f"https://drive.google.com/uc?export=download&id={file_id}&confirm=t&uuid=random"
