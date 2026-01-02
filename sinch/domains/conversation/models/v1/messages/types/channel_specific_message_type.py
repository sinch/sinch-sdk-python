from typing import Literal, Union
from pydantic import StrictStr


ChannelSpecificMessageType = Union[
    Literal[
        "FLOWS",
        "ORDER_DETAILS",
        "ORDER_STATUS",
        "COMMERCE",
        "CAROUSEL_COMMERCE",
    ],
    StrictStr,
]
