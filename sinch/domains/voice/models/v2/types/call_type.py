from typing import Literal, Union

from pydantic import StrictStr

CallType = Union[Literal["PHONE", "SIP", "STREAM", "VOICE_RELAY"], StrictStr]
