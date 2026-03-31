from typing import TypedDict
from typing_extensions import NotRequired


class ChoiceMessagePropertiesDict(TypedDict):
    """
    Additional properties for ChoiceMessage (whatsapp_footer).
    CardMessage uses MessagePropertiesDict with whatsapp_header.
    """

    whatsapp_footer: NotRequired[str]
