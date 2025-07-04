from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class BaseStatus:
    status: Literal[
        "queued",
        "processing",
        "start_generation",
        "timeout",
        "error",
    ]


@dataclass
class QueuedStatus(BaseStatus):
    position: int
    queue_length: int
    wait_min: int
    prompt_id: str


@dataclass
class ProcessingStatus(BaseStatus):
    wait_min: int
    prompt_id: str


@dataclass
class StartGenerationStatus(BaseStatus):
    wait_min: int
    prompt_id: str


@dataclass
class TimeoutStatus(BaseStatus):
    pass


@dataclass
class ErrorStatus(BaseStatus):
    pass


NSFWVideoStatus = (
    QueuedStatus
    | ProcessingStatus
    | StartGenerationStatus
    | TimeoutStatus
    | ErrorStatus
)


@dataclass
class DownloadedVideo:
    path: Optional[str]
    caption: Optional[str]
