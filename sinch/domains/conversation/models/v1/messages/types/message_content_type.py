from typing import Literal, Union
from pydantic import StrictStr

MessageContentType = Union[
    Literal["CONTENT_UNKNOWN", "CONTENT_MARKETING", "CONTENT_NOTIFICATION"],
    StrictStr,
]
