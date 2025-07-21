from bot.services.iloveapi.client.api_client import ILoveAPI
from bot.services.iloveapi.client.interfaces import (
    DownloaderProtocol,
    ProcesserProtocol,
    StarterProtocol,
    UploaderProtocol,
)
from bot.services.iloveapi.files.downloader import ILoveAPIDownloader
from bot.services.iloveapi.files.uploader import ILoveAPIUploader
from bot.services.iloveapi.services.processer import ILoveAPIProcesser
from bot.services.iloveapi.services.starter import ILoveAPIStarter
from bot.services.iloveapi.task_service import ILoveAPITaskService
from bot.settings import settings


def get_iloveapi_service(
    uploader: UploaderProtocol = None,
    downloader: DownloaderProtocol = None,
    processer: ProcesserProtocol = None,
    starter: StarterProtocol = None,
    api_url: str = None,
    public_key: str = None,
):
    api_url = api_url or settings.ILOVEAPI_API_URL
    public_key = public_key or settings.PUBLIC_ILOVEAPI_API_KEY
    api = ILoveAPI(api_url, public_key)
    starter = starter or ILoveAPIStarter(api)
    uploader = uploader or ILoveAPIUploader(api)
    processer = processer or ILoveAPIProcesser(api)
    downloader = downloader or ILoveAPIDownloader(api)
    return ILoveAPITaskService(api, starter, uploader, processer, downloader)
