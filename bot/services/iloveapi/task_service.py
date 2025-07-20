from bot.services.iloveapi.api_client import ILoveAPI
from bot.services.iloveapi.processer import ILoveAPIProcesser
from bot.services.iloveapi.starter import ILoveAPIStarter
from bot.services.iloveapi.types import ToolType
from bot.services.iloveapi.uploader import ILoveAPIUploader


class ILoveAPITaskService:
    def __init__(self, api_url: str, public_key: str):
        self.api = ILoveAPI(api_url, public_key)
        self.starter = ILoveAPIStarter(self.api)
        self.uploader = ILoveAPIUploader(self.api)
        self.processer = ILoveAPIProcesser(self.api)

    async def run_image_task(self, tool: ToolType, file_path: str, tool_data: dict) -> dict:
        # 1. Стартуем задачу
        task_json = await self.starter.start_task(tool)
        server = task_json["server"]
        task_id = task_json["task"]

        # 2. Загружаем файл
        server_filename = await self.uploader.upload(server, task_id, file_path)
        files = [{"server_filename": server_filename, "filename": file_path}]

        # 3. Запускаем обработку
        result = await self.processer.process(server, task_id, tool, files, tool_data)
        return result

    # Можно добавить методы-обёртки для конкретных задач:
    async def resize_image(self, file_path: str, width: int, height: int) -> dict:
        return await self.run_image_task(
            ToolType.RESIZE_IMAGE,
            file_path,
            {"pixels_width": width, "pixels_height": height}
        )