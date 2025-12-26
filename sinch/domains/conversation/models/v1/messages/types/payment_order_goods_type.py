from typing import Literal, Union
from pydantic import StrictStr

PaymentOrderGoodsType = Union[
    Literal["digital-goods", "physical-goods"],
    StrictStr,
]
