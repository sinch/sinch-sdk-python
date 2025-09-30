from typing import Union, Literal
from pydantic import StrictStr


NumberSearchPatternType = Union[Literal["START", "CONTAINS", "END"], StrictStr]
