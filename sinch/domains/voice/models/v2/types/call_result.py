from typing import Literal, Union

from pydantic import StrictStr

CallResult = Union[
    Literal[
        "QUEUED",
        "INITIATED",
        "IN_PROGRESS",
        "COMPLETED",
        "REJECTED",
        "NO_ANSWER",
        "CANCEL",
        "BUSY",
        "FAILED",
    ],
    StrictStr,
]
