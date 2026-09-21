from typing import Literal, Union

from pydantic import StrictStr

GetChannelProfileConversationChannelType = Union[
    Literal["MESSENGER", "INSTAGRAM", "VIBER", "LINE"], StrictStr
]
