from typing import Literal, Union
from pydantic import StrictStr


MessageSourceType = Union[
    Literal["CONVERSATION_SOURCE", "DISPATCH_SOURCE"], StrictStr
]
