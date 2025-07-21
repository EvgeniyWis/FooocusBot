from bot.services.iloveapi.api_client import ILoveAPI
from bot.services.iloveapi.downloader import ILoveAPIDownloader
from bot.services.iloveapi.processer import ILoveAPIProcesser
from bot.services.iloveapi.starter import ILoveAPIStarter
from bot.services.iloveapi.task_service import ILoveAPITaskService
from bot.services.iloveapi.uploader import ILoveAPIUploader
from bot.settings import settings


def get_iloveapi_service():
    api = ILoveAPI(settings.ILOVEAPI_API_URL, settings.PUBLIC_ILOVEAPI_API_KEY)
    starter = ILoveAPIStarter(api)
    uploader = ILoveAPIUploader(api)
    processer = ILoveAPIProcesser(api)
    downloader = ILoveAPIDownloader(api)
    task_service = ILoveAPITaskService(api, starter, uploader, processer, downloader)
    return task_service
