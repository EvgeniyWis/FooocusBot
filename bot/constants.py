from pathlib import Path
from typing import Final

BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent
TEMP_IMAGE_FILES_DIR: Final[Path] = BASE_DIR / "bot" / "temp" / "images"
FACEFUSION_DIR: Final[Path] = BASE_DIR / ".assets"
TEMP_FOLDER_PATH: Final[Path] = FACEFUSION_DIR / "images" / "temp"
FACEFUSION_RESULTS_DIR: Final[Path] = FACEFUSION_DIR / "images" / "results"
VIDEOS_TEMP_DIR: Final[Path] = BASE_DIR / "bot" / "temp" / "videos"
TEMP_DIR: Final[Path] = BASE_DIR / "temp"
