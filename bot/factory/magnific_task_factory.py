from bot.services.freepik.services.magnific.client.api_client import (
    MagnificAPI,
)
from bot.services.freepik.services.magnific.facade.task_facade import (
    TaskFacade,
)
from bot.services.freepik.services.magnific.interfaces.protocols import (
    StatusServiceProtocol,
    UpscalerProtocol,
)
from bot.services.freepik.services.magnific.services.status_service import (
    StatusService,
)
from bot.services.freepik.services.magnific.services.upscaler import (
    UpscalerService,
)
from bot.app.config.settings import settings


def get_magnific_task_factory(
    api_url: str = None,
    api_key: str = None,
    upscaler: UpscalerProtocol = None,
    status_service: StatusServiceProtocol = None,
):
    api_url = api_url or settings.FREEPIK_API_URL
    api_key = api_key or settings.FREEPIK_API_KEY
    magnific_api = MagnificAPI(api_url, api_key)
    upscaler = upscaler or UpscalerService(magnific_api)
    status_service = status_service or StatusService(magnific_api)
    return TaskFacade(
        api=magnific_api,
        upscaler=upscaler,
        status_service=status_service,
    )
