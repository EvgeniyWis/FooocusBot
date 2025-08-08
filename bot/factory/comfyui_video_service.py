import bot.app.config.constants as contants
from bot.services.comfyui.video_service import ComfyUIVideoService
from bot.app.config.settings import settings


def get_video_service():
    video_service = ComfyUIVideoService(
        settings.COMFYUI_API_URL,
        contants.COMFYUI_WORKFLOW_TEMPLATE_PATH,
        contants.COMFYUI_AVG_TIMES_METRICS_PATH,
    )
    return video_service
