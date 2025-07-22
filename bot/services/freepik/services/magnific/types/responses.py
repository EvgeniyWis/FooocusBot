from typing import List, Literal, Optional, TypedDict

Status = Literal["IN_PROGRESS", "COMPLETED", "FAILED", "CREATED"]

class MagnificTaskResponse(TypedDict):
    generated: List[str]
    task_id: str
    status: Status

class MagnificStatusResponse(TypedDict, total=False):
    generated: Optional[List[str]]
    task_id: str
    status: Status

class MagnificErrorResponse(TypedDict, total=False):
    error: str
    message: str