from typing import Literal, Union

from pydantic import StrictStr
from typing_extensions import Annotated, deprecated

VoiceApplicationType = Annotated[
    Union[Literal["RTC", "EST", "FAX"], StrictStr],
    deprecated(
        "VoiceApplicationType is deprecated since 2.2.0 because of unused"
        "it will be removed in 3.0."
    ),
]
