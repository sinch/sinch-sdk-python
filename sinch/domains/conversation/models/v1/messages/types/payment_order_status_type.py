from typing import Literal, Union
from pydantic import StrictStr


PaymentOrderStatusType = Union[
    Literal[
        "pending",
        "processing",
        "partially-shipped",
        "shipped",
        "completed",
        "canceled",
    ],
    StrictStr,
]
