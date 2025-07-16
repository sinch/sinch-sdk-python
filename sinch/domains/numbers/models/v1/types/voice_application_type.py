from typing import Annotated, Literal, Union
from pydantic import Field, StrictStr


VoiceApplicationTypeValues = Union[Literal[
    "RTC",
    "EST",
    "FAX"
], StrictStr]

VoiceApplicationType = Annotated[
    VoiceApplicationTypeValues,
    Field(default=None)
]
