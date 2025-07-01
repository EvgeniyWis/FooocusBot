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

    def prepare(self, prompt: str, image_name: str) -> dict:
        logger.info("Загрузка шаблона воркфлоу")
        try:
            with open(self.workflow_template_path) as f:
                template = json.load(f)

            workflow = copy.deepcopy(template["prompt"])
            workflow["220"]["inputs"]["text"] = prompt
            workflow["126"]["inputs"]["image"] = image_name

            logger.debug(
                f"Подготовлен воркфлоу с промптом: '{prompt}' и изображением: {image_name}",
            )
            return workflow
        except Exception as e:
            logger.error(f"Ошибка при подготовке воркфлоу: {str(e)}")
            raise
