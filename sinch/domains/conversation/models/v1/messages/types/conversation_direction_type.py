from typing import Literal, Union
from pydantic import StrictStr

ConversationDirectionType = Union[
    Literal["TO_APP", "TO_CONTACT"],
    StrictStr,
]
