from typing import Union, Literal
from pydantic import StrictStr


VoIPProbabilityType = Union[
    Literal["Unknown", "High", "Likely", "Low"], StrictStr
]
