from pathlib import Path
from typing import Final

# Указываем корень проекта (папка FooocusBot)
BASE_DIR: Final[Path] = Path(__file__).resolve().parents[2]
TEMP_FILES_DIR: Final[Path] = BASE_DIR / "bot" / "temp"
TEMP_IMAGE_FILES_DIR: Final[Path] = BASE_DIR / "bot" / "temp" / "images"
FACEFUSION_DIR: Final[Path] = BASE_DIR / ".assets"
FACEFUSION_TEMP_IMAGES_FOLDER_PATH: Final[Path] = FACEFUSION_DIR / "images" / "temp"
FACEFUSION_RESULTS_DIR: Final[Path] = FACEFUSION_DIR / "images" / "results"
TEMP_VIDEOS_FILES_DIR: Final[Path] = BASE_DIR / "bot" / "temp" / "videos"
TEMP_DIR: Final[Path] = BASE_DIR / "temp"
MOCK_VIDEO_PATH: Final[Path] = BASE_DIR / "bot" / "assets" / "mocks" / "mock_video.mp4"
COMFYUI_WORKFLOW_TEMPLATE_PATH: Final[Path] = (
    BASE_DIR / "bot" / "assets" / "comfyui" / "comfyui_workflows" / "wan.json"
)
COMFYUI_AVG_TIMES_METRICS_PATH: Final[Path] = (
    BASE_DIR / "bot" / "assets" / "comfyui" / "avg_times_metrics.json"
)
COMFYUI_HEATING_IMAGES_PATH: Final[Path] = (
    BASE_DIR / "bot" / "assets" / "comfyui" / "heating" / "img"
)

# Не может быть больше 9!
MULTI_IMAGE_NUMBER: Final[int] = 9 