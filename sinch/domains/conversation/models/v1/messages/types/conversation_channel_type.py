from typing import Literal, Union
from pydantic import StrictStr

ConversationChannelType = Union[
    Literal[
        "WHATSAPP",
        "RCS",
        "SMS",
        "MESSENGER",
        "VIBERBM",
        "MMS",
        "INSTAGRAM",
        "TELEGRAM",
        "KAKAOTALK",
        "KAKAOTALKCHAT",
        "LINE",
        "WECHAT",
        "APPLEBC",
    ],
    StrictStr,
]
