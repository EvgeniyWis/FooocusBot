from enum import Enum


class ProcessImageStep(str, Enum):
    UPSCALE = "upscale"
    SECOND_UPSCALE = "second_upscale"
    FACEFUSION = "faceswap"
    SAVE = "save"
