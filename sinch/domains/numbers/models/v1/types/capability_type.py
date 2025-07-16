from pydantic import Field, StrictStr
from typing import Annotated, Literal, Union

CapabilityTypeValues = Union[Literal["SMS", "VOICE"], StrictStr]

CapabilityType = Annotated[
    CapabilityTypeValues,
    Field(default=None)
]
