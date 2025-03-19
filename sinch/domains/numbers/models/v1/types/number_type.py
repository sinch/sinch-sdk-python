from typing import Union, Literal, Annotated
from pydantic import StrictStr, Field

NumberTypeValues = Union[Literal["MOBILE", "LOCAL", "TOLL_FREE"], StrictStr]


NumberType = Annotated[
    NumberTypeValues,
    Field(default=None)
]
