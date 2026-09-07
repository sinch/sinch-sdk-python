from typing import Literal, Union

from pydantic import StrictStr

RecordingType = Union[Literal["COMBINED", "INBOUND", "OUTBOUND"], StrictStr]
