from typing import Literal, Union
from pydantic import StrictStr

ProcessingModeType = Union[
    Literal["CONVERSATION", "DISPATCH"],
    StrictStr,
]
