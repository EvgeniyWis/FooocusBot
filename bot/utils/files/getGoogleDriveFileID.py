import re

def getGoogleDriveFileID(url: str) -> str | None:
    pattern = r'(?:/file/d/|id=)([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)
    return match.group(1) if match else None