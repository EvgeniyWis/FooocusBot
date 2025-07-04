from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class QueuedStatus:
    status: Literal["queued"]
    position: int
    queue_length: int
    wait_min: int
    prompt_id: str


@dataclass
class ProcessingStatus:
    status: Literal["processing"]
    wait_min: int
    prompt_id: str


@dataclass
class StartGenerationStatus:
    status: Literal["start_generation"]
    wait_min: int
    prompt_id: str


@dataclass
class TimeoutStatus:
    status: Literal["timeout"]


@dataclass
class ErrorStatus:
    status: Literal["error"]


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
