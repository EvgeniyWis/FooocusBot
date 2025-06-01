import re


def getGoogleDriveFileID(url: str) -> str | None:
    try:
        # Очищаем URL от лишнего текста
        url = re.sub(r'\s*-\s*.*?:\s*', '', url)
        
        # Убираем все пробелы
        url = url.replace(' ', '')
        
        pattern = r"(?:/file/d/|id=|/d/)([a-zA-Z0-9_-]+)"
        match = re.search(pattern, url)
        return match.group(1) if match else None
    except Exception as e:
        return None
