from typing import Literal, Optional, TypedDict

ImagesToolType = Literal[
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

ToolType = ImagesToolType

class FileFormat(TypedDict):
    server_filename: str
    filename: str
    rotate: Optional[int]
    password: Optional[str]