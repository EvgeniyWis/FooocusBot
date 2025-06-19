from pathlib import Path
from typing import Final

BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent
TEMP_IMAGE_FILES_DIR: Final[Path] = BASE_DIR / "bot" / "temp" / "images"
FACEFUSION_DIR: Final[Path] = BASE_DIR.parent / "facefusion-docker"
TEMP_FOLDER_PATH: Final[Path] = FACEFUSION_DIR / ".assets" / "images" / "temp"
VIDEOS_TEMP_DIR: Final[Path] = BASE_DIR / "bot" / "temp" / "videos"
FACEFUSION_RESULTS_DIR: Final[Path] = (
    FACEFUSION_DIR / ".assets" / "images" / "results"
)
TEMP_DIR: Final[Path] = BASE_DIR / "temp"
