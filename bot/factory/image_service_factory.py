from bot.services.iloveapi.adapters.task.downloader import Downloader
from bot.services.iloveapi.adapters.task.processor import Processor
from bot.services.iloveapi.adapters.task.starter import Starter
from bot.services.iloveapi.adapters.task.uploader import Uploader
from bot.services.iloveapi.client.api_client import ILoveAPI
from bot.services.iloveapi.client.interfaces import (
    ResizerProtocol,
    UpscalerProtocol,
)
from bot.services.iloveapi.facade.task_facade import TaskFacade
from bot.services.iloveapi.services.resizer import ResizeImageService
from bot.services.iloveapi.services.upscaler import UpscaleImageService
from bot.settings import settings


def create_task_facade() -> TaskFacade:
    api = ILoveAPI(settings.ILOVEAPI_API_URL, settings.PUBLIC_ILOVEAPI_API_KEY)
    starter = Starter(api)
    uploader = Uploader(api)
    processor = Processor(api)
    downloader = Downloader(api)
    return TaskFacade(api, starter, uploader, processor, downloader)

def create_resizer() -> ResizerProtocol:
    task_facade = create_task_facade()
    return ResizeImageService(task_facade)

def create_upscaler() -> UpscalerProtocol:
    task_facade = create_task_facade()
    return UpscaleImageService(task_facade)
