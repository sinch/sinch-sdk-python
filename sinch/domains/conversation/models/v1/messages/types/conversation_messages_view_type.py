from typing import Literal, Union
from pydantic import StrictStr


ConversationMessagesViewType = Union[
    Literal["WITH_METADATA", "WITHOUT_METADATA"],
    StrictStr,
]
