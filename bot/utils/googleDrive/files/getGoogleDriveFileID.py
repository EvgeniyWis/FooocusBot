import re
from bot.app.core.logging import logger


def getGoogleDriveFileID(url: str) -> str | None:
    try:
        # Очищаем URL от лишнего текста
        url = re.sub(r'\s*-\s*.*?:\s*', '', url)
        
        # Убираем все пробелы
        url = url.replace(' ', '')
        
        pattern = r"(?:/file/d/|id=|/d/)([a-zA-Z0-9_-]+)"
        match = re.search(pattern, url)

        logger.info(f"ID файла, полученный из Google Drive где url: {url}: {match.group(1)}")
        return match.group(1) if match else None
    except Exception as e:
        raise Exception(f"Произошла ошибка при получении ID файла из Google Drive: {e}")