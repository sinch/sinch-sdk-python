from pydantic import conlist, Field, StrictStr
from typing import Annotated, Literal, Union

CapabilityTypeValuesList = conlist(Union[Literal["SMS", "VOICE"], StrictStr], min_length=1)

CapabilityType = Annotated[
    CapabilityTypeValuesList,
    Field(default=None)
]
