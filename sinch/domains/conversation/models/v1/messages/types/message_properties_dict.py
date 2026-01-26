from typing import TypedDict
from typing_extensions import NotRequired


class MessagePropertiesDict(TypedDict):
    whatsapp_header: NotRequired[str]
