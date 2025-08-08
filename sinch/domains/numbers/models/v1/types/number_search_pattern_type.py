from typing import Union, Literal, Annotated
from pydantic import StrictStr, Field


NumberSearchPatternTypeValues = Union[Literal["START", "CONTAINS", "END"], StrictStr]

NumberSearchPatternType = Annotated[
    NumberSearchPatternTypeValues,
    Field(default=None)
]
