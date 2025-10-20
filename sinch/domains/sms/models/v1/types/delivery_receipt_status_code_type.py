from typing import Literal, Union
from pydantic import StrictStr


DeliveryReceiptStatusCodeType = Union[
    Literal[
        400,
        401,
        402,
        403,
        404,
        405,
        406,
        407,
        408,
        410,
        411,
        412,
        413,
        414,
        415,
        416,
        417,
        418,
    ],
    StrictStr,
]
