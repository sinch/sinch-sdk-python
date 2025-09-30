from typing import Literal, Union
from pydantic import StrictStr


VoiceApplicationType = Union[Literal[
    "RTC",
    "EST",
    "FAX"
], StrictStr]
