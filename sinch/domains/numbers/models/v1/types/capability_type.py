from pydantic import StrictStr
from typing import Literal, Union


CapabilityType = Union[Literal["SMS", "VOICE"], StrictStr]
