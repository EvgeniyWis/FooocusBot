import copy
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from bot.logger import logger


@dataclass
class WorkflowNodes:
    PROMPT_NODE: str = "220"
    IMAGE_NODE: str = "126"
    VIDEO_LENGTH_NODE: str = "50"


class ComfyUIWorkflowPreparer:
    FPS: float = 16.25  # Фиксированное значение для конвертации секунд в кадры

    def __init__(self, workflow_template_path: str | Path):
        self.workflow_template_path = Path(workflow_template_path)
        logger.info(
            f"Инициализирован подготовщик воркфлоу с шаблоном: {workflow_template_path}",
        )

    def _load_template(self) -> dict:
        """Загружает шаблон воркфлоу из файла."""
        try:
            with open(self.workflow_template_path) as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(
                f"Шаблон воркфлоу не найден: {self.workflow_template_path}",
            )
            raise
        except json.JSONDecodeError:
            logger.error(
                f"Ошибка парсинга JSON в шаблоне: {self.workflow_template_path}",
            )
            raise
        except Exception as e:
            logger.error(f"Неожиданная ошибка при загрузке шаблона: {str(e)}")
            raise

    def _convert_seconds_to_frames(self, seconds: int) -> int:
        """Конвертирует секунды в количество кадров."""
        return int(seconds * self.FPS)

    def prepare(
        self,
        prompt: str,
        image_name: str,
        seconds: Optional[int] = None,
    ) -> dict:
        """
        Подготавливает воркфлоу для генерации.

        Args:
            prompt: Промпт для генерации
            image_name: Имя изображения
            seconds: Длительность видео в секундах (опционально)

        Returns:
            dict: Подготовленный воркфлоу
        """
        logger.info(
            f"Подготовка воркфлоу: prompt={prompt}, image={image_name}, seconds={seconds}",
        )
        try:
            workflow = copy.deepcopy(self._load_template())
            workflow[WorkflowNodes.PROMPT_NODE]["inputs"]["text"] = prompt
            workflow[WorkflowNodes.IMAGE_NODE]["inputs"]["image"] = image_name
            if seconds is not None:
                length = self._convert_seconds_to_frames(seconds)
                if (
                    WorkflowNodes.VIDEO_LENGTH_NODE in workflow
                    and "inputs" in workflow[WorkflowNodes.VIDEO_LENGTH_NODE]
                ):
                    workflow[WorkflowNodes.VIDEO_LENGTH_NODE]["inputs"][
                        "length"
                    ] = length
                    logger.info(
                        f"Установлена длительность видео: {seconds}с ({length} кадров)",
                    )

            return workflow
        except Exception as e:
            logger.error(f"Ошибка при подготовке воркфлоу: {str(e)}")
            raise
