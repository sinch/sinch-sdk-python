from typing import Literal, Union
from pydantic import StrictStr

ProcessingStrategyType = Union[
    Literal["DEFAULT", "DISPATCH_ONLY"],
    StrictStr,
]
