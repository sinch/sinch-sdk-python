from typing import Literal, Union

from pydantic import StrictStr


MessageDeliveryStatusType = Union[
    Literal[
        "QUEUED_ON_CHANNEL",
        "DELIVERED",
        "READ",
        "FAILED",
        "SWITCHING_CHANNEL",
    ],
    StrictStr,
]
