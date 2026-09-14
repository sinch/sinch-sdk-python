from typing import Literal, Union

from pydantic import StrictStr

OriginationType = Union[Literal["PHONE", "SIP", "SERVER"], StrictStr]
