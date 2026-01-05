from typing import Literal, Union
from pydantic import StrictStr

ConversationDirectionType = Union[
    Literal["UNDEFINED_DIRECTION", "TO_APP", "TO_CONTACT"],
    StrictStr,
]
