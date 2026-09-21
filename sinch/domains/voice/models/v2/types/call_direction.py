from typing import Literal, Union

from pydantic import StrictStr

CallDirection = Union[Literal["INBOUND", "OUTBOUND"], StrictStr]
