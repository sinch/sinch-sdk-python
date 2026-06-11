from typing import Literal
from pydantic import Field, StrictStr
from sinch.domains.sms.models.v1.shared.base_mo_message import BaseMOMessage


class MOTextMessage(BaseMOMessage):
    body: StrictStr = Field(
        ...,
        description="The incoming message body. Maximum 2000 characters.",
    )
    type: Literal["mo_text"] = Field(
        ..., description="The type of incoming message. Regular SMS."
    )
