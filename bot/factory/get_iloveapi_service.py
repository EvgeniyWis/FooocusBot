from bot.services.iloveapi.api_client import ILoveAPI
from bot.services.iloveapi.downloader import ILoveAPIDownloader
from bot.services.iloveapi.interfaces import (
    DownloaderProtocol,
    ProcesserProtocol,
    StarterProtocol,
    UploaderProtocol,
)
from bot.services.iloveapi.processer import ILoveAPIProcesser
from bot.services.iloveapi.starter import ILoveAPIStarter
from bot.services.iloveapi.task_service import ILoveAPITaskService
from bot.services.iloveapi.uploader import ILoveAPIUploader
from bot.settings import settings

# Singleton instance
_iloveapi_service_instance = None

def get_iloveapi_service(
    uploader: UploaderProtocol = None,
    downloader: DownloaderProtocol = None,
    processer: ProcesserProtocol = None,
    starter: StarterProtocol = None,
):
    global _iloveapi_service_instance
    if _iloveapi_service_instance is None:
        api = ILoveAPI(settings.ILOVEAPI_API_URL, settings.PUBLIC_ILOVEAPI_API_KEY)
        starter = starter or ILoveAPIStarter(api)
        uploader = uploader or ILoveAPIUploader(api)
        processer = processer or ILoveAPIProcesser(api)
        downloader = downloader or ILoveAPIDownloader(api)
        _iloveapi_service_instance = ILoveAPITaskService(api, starter, uploader, processer, downloader)
    return _iloveapi_service_instance
