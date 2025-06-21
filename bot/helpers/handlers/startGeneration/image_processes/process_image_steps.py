from enum import Enum

class ProcessImageStep(str, Enum):
    UPSCALE = "upscale"
    FACEFUSION = "faceswap"
    SAVE = "save"
