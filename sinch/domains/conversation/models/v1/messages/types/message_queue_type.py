from typing import Literal, Union
from pydantic import StrictStr

MessageQueueType = Union[
    Literal["NORMAL_PRIORITY", "HIGH_PRIORITY"],
    StrictStr,
]
