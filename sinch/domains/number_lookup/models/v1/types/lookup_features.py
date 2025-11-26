from typing import Union, Literal
from pydantic import StrictStr


LookupFeaturesType = Union[
    Literal["LineType", "SimSwap", "VoIPDetection", "RND"], StrictStr
]
