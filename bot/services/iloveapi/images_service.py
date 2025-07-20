
from bot.services.iloveapi.api_client import ILoveAPI
from bot.services.iloveapi.processer import ILoveAPIProcesser
from bot.services.iloveapi.starter import ILoveAPIStarter
from bot.services.iloveapi.types import ToolType
from bot.services.iloveapi.uploader import ILoveAPIUploader


class ILoveAPIImagesService:
    def __init__(self, api_url: str):
        self.api = ILoveAPI(api_url)
        self.starter = ILoveAPIStarter(self.api)
        self.uploader = ILoveAPIUploader(self.api)
        self.processer = ILoveAPIProcesser(self.api)

    async def resize(self, pixels_width: int, pixels_height: int, file: str) -> str:
        # Получаем данные со старта задачи
        task_json = await self.starter.start_task(ToolType.RESIZE_IMAGE)
        server = task_json["server"]
        task_id = task_json["task"]

        # Загружаем изображение
        server_filename = await self.uploader.upload(server, task_id, file)

        # Обрабатываем изображение
        tool_data = {
            "pixels_width": pixels_width,
            "pixels_height": pixels_height,
        }
        process_json = await self.processer.process(server, task_id,
        ToolType.RESIZE_IMAGE, [server_filename], tool_data)

        return process_json