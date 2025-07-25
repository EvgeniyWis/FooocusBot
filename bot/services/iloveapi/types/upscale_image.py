from typing import Literal, TypedDict

UpscaleMultiplier = Literal[2, 4]

class ToolDataUpscaleImage(TypedDict):
    multiplier: UpscaleMultiplier
