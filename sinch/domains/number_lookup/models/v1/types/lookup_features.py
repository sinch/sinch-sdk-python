from typing import Union, Literal
from pydantic import StrictStr


LookupFeatures = Union[
    Literal["LineType", "SimSwap", "VoIPDetection", "RND"], StrictStr
]
