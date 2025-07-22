from typing import Literal, Optional, TypedDict

ToolType = Literal[
    "compressimage",
    "cropimage",
    "convertimage",
    "removebackgroundimage",
    "repairimage",
    "resizeimage",
    "rotateimage",
    "upscaleimage",
    "watermarkimage",
]

class TaskFileFormat(TypedDict):
    server_filename: str
    filename: str
    rotate: Optional[int]
    password: Optional[str]

class ToolDataResizeImage(TypedDict):
    pixels_width: int
    pixels_height: int
    maintain_ratio: bool

class StartTaskResponse(TypedDict):
    server: str
    task: str
    remaining_credits: int

class UploadResponse(TypedDict):
    server_filename: str