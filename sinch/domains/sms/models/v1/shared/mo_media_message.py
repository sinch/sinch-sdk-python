from typing import Literal
from pydantic import Field
from sinch.domains.sms.models.v1.shared.base_mo_message import BaseMOMessage
from sinch.domains.sms.models.v1.shared.mo_media_body import MOMediaBody


class MOMediaMessage(BaseMOMessage):
    body: MOMediaBody = Field(
        ...,
        description="The media message body.",
    )
    type: Literal["mo_media"] = Field(
        ..., description="The type of incoming message. MMS."
    )
