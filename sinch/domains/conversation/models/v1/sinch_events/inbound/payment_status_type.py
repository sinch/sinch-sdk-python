from typing import Literal, Union

from pydantic import StrictStr

PaymentStatusType = Union[
    Literal[
        "PAYMENT_STATUS_UNKNOWN",
        "PAYMENT_STATUS_NEW",
        "PAYMENT_STATUS_PENDING",
        "PAYMENT_STATUS_CAPTURED",
        "PAYMENT_STATUS_CANCELED",
        "PAYMENT_STATUS_FAILED",
    ],
    StrictStr,
]
