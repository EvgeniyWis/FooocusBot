import copy
import json
from pathlib import Path

from bot.logger import logger


class ComfyUIWorkflowPreparer:
    def __init__(self, workflow_template_path: str | Path):
        self.workflow_template_path = Path(workflow_template_path)
        logger.info(
            f"Инициализирован подготовщик воркфлоу с шаблоном: {workflow_template_path}",
        )

    def prepare(
        self,
        prompt: str,
        image_name: str,
        seconds: int = None,
    ) -> dict:
        logger.info("Загрузка шаблона воркфлоу")
        try:
            with open(self.workflow_template_path) as f:
                template = json.load(f)

            workflow = copy.deepcopy(template)
            workflow["220"]["inputs"]["text"] = prompt
            workflow["126"]["inputs"]["image"] = image_name
            if seconds is not None:
                fps = 16.25  # фиксированное значение
                length = int(seconds * fps)
                if "50" in workflow and "inputs" in workflow["50"]:
                    workflow["50"]["inputs"]["length"] = length

            logger.debug(
                f"Подготовлен воркфлоу с промптом: '{prompt}', изображением: {image_name}, длиной: {length}",
            )
            return workflow
        except Exception as e:
            logger.error(f"Ошибка при подготовке воркфлоу: {str(e)}")
            raise
