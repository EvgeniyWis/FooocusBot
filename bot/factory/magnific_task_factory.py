from bot.services.freepik.services.magnific.client.api_client import (
    MagnificAPI,
)
from bot.services.freepik.services.magnific.client.interfaces import (
    StatusServiceProtocol,
    UpscalerProtocol,
)
from bot.services.freepik.services.magnific.facade.task_facade import (
    MagnificTaskFacade,
)
from bot.services.freepik.services.magnific.services.status_service import (
    MagnificStatusService,
)
from bot.services.freepik.services.magnific.services.upscaler import (
    MagnificUpscaler,
)
from bot.settings import settings


def get_magnific_task_factory(
    api_url: str = None,
    api_key: str = None,
    upscaler: UpscalerProtocol = None,
    status_service: StatusServiceProtocol = None,
):
    api_url = api_url or settings.FREEPIK_API_URL
    api_key = api_key or settings.FREEPIK_API_KEY
    magnific_api = MagnificAPI(api_url, api_key)
    upscaler = upscaler or MagnificUpscaler(magnific_api)
    status_service = status_service or MagnificStatusService(magnific_api)
    return MagnificTaskFacade(
        api=magnific_api,
        upscaler=upscaler,
        status_service=status_service,
    )
