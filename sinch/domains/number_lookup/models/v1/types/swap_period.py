from typing import Union, Literal
from pydantic import StrictStr


SwapPeriodType = Union[
    Literal[
        "Undefined",
        "SP4H",
        "SP12H",
        "SP24H",
        "SP48H",
        "SP5D",
        "SP7D",
        "SP14D",
        "SP30D",
        "SPMAX",
    ],
    StrictStr,
]
