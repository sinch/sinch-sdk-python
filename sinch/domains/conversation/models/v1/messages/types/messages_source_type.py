from typing import Literal, Union
from pydantic import StrictStr


MessagesSourceType = Union[
    Literal["CONVERSATION_SOURCE", "DISPATCH_SOURCE"], StrictStr
]
