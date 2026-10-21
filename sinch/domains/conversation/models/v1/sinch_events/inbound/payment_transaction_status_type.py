from typing import Literal, Union

from pydantic import StrictStr

PaymentTransactionStatusType = Union[
    Literal[
        "PAYMENT_STATUS_TRANSACTION_UNKNOWN",
        "PAYMENT_STATUS_TRANSACTION_PENDING",
        "PAYMENT_STATUS_TRANSACTION_FAILED",
        "PAYMENT_STATUS_TRANSACTION_SUCCESS",
        "PAYMENT_STATUS_TRANSACTION_CANCELED",
    ],
    StrictStr,
]
