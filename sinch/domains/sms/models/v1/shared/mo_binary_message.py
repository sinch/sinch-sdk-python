from typing import Literal
from pydantic import Field, StrictStr
from sinch.domains.sms.models.v1.shared.base_mo_message import BaseMOMessage


class MOBinaryMessage(BaseMOMessage):
    body: StrictStr = Field(
        ..., description="The incoming message body (Base64 encoded)."
    )
    type: Literal["mo_binary"] = Field(
        ..., description="The type of incoming message. Binary SMS."
    )
    udh: StrictStr = Field(
        ..., description="The UDH header of a binary message HEX encoded."
    )
