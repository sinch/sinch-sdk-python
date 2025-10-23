from typing import Literal, Union
from pydantic import StrictStr


DeliveryStatusType = Union[
    Literal[
        "QUEUED",
        "DISPATCHED",
        "ABORTED",
        "CANCELLED",
        "FAILED",
        "DELIVERED",
        "EXPIRED",
        "REJECTED",
        "DELETED",
        "UNKNOWN",
    ],
    StrictStr,
]
