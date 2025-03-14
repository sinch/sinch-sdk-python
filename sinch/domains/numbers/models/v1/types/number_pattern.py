from typing import TypedDict
from typing_extensions import NotRequired
from typing import Union, Literal, Annotated
from pydantic import StrictStr, Field


NumberSearchPatternTypeValues = Union[Literal["START", "CONTAINS", "END"], StrictStr]

NumberSearchPatternType = Annotated[
    NumberSearchPatternTypeValues,
    Field(default=None)
]


class NumberPatternDict(TypedDict):
    pattern: NotRequired[str]
    search_pattern: NotRequired[NumberSearchPatternTypeValues]
