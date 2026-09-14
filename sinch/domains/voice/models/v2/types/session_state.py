from typing import Literal, Union

from pydantic import StrictStr

SessionState = Union[
    Literal["QUEUED", "IN_PROGRESS", "COMPLETED", "EXPIRED"], StrictStr
]
