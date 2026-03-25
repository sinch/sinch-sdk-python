from typing import Literal, Union
from pydantic import StrictStr


DeliveryStatusType = Union[
    Literal[
        "QUEUED_ON_CHANNEL",
        "DELIVERED",
        "READ",
        "FAILED",
        "SWITCHING_CHANNEL",
    ],
    StrictStr,
]
