from typing import Literal, Union
from pydantic import StrictStr

PaymentOrderType = Union[
    Literal["br", "sg"],
    StrictStr,
]
