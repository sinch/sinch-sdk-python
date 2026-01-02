from typing import Literal, Union
from pydantic import StrictStr

CardHeightType = Union[
    Literal["UNSPECIFIED_HEIGHT", "SHORT", "MEDIUM", "TALL"],
    StrictStr,
]
