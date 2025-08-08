from bot.app.config.constants import BASE_DIR
from bot.app.config.settings import settings

MOCK_LINK_FOR_SAVE_IMAGE = settings.MOCK_LINK_FOR_SAVE_IMAGE
MOCK_LINK_FOR_SAVE_VIDEO = settings.MOCK_LINK_FOR_SAVE_VIDEO
MOCK_FACEFUSION_PATH = (
    BASE_DIR / "bot" / "assets" / "mocks" / "mock_image.jpg"
)
