from enum import Enum
from typing import Optional, TypedDict


class ImagesToolType(Enum):
    COMPRESS_IMAGE = "compressimage"
    CROP_IMAGE = "cropimage"
    CONVERT_IMAGE = "convertimage"
    REMOVE_BACKGROUND_IMAGE = "removebackgroundimage"
    REPAIR_IMAGE = "repairimage"
    RESIZE_IMAGE = "resizeimage"
    ROTATE_IMAGE = "rotateimage"
    UPSCALE_IMAGE = "upscaleimage"
    WATERMARK_IMAGE = "watermarkimage"


ToolType = ImagesToolType

class FileFormat(TypedDict):
    server_filename: str
    filename: str
    rotate: Optional[int]
    password: Optional[str]