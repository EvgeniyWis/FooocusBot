from dataclasses import asdict, dataclass
from typing import Any, Dict


class BaseTaskDTO:
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseTaskDTO":
        return cls(**data)


@dataclass
class TaskImageBlockDTO(BaseTaskDTO):
    job_id: str
    user_id: int
    message_id: int
    model_name: str
    setting_number: int | str
    is_test_generation: bool
    check_other_jobs: bool
    chat_id: int


@dataclass
class TaskProcessImageDTO(BaseTaskDTO):
    user_id: int
    chat_id: int
    message_id: int
    callback_data: str
    model_name: str
    image_index: int


@dataclass
class TaskProcessVideoDTO(BaseTaskDTO):
    user_id: int
    chat_id: int
    message_id: int
    callback_data: str
    model_name: str
    prompt: str
    image_url: str
    image_path: str
