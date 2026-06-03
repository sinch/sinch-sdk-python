from datetime import datetime
from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)


class BaseMOMessage(BaseModelConfigurationResponse):
    from_: StrictStr = Field(
        ...,
        alias="from",
        description="The phone number that sent the message.",
    )
    id: StrictStr = Field(..., description="The ID of this inbound message.")
    received_at: datetime = Field(
        ...,
        description="When the system received the message. Formatted as ISO-8601: YYYY-MM-DDThh:mm:ss.SSSZ.",
    )
    to: StrictStr = Field(
        ...,
        description="The Sinch phone number or short code to which the message was sent.",
    )
    client_reference: Optional[StrictStr] = Field(
        default=None,
        description="If this inbound message is in response to a previously sent message that contained a client reference, then this field contains that client reference. Utilizing this feature requires additional setup on your account.",
    )
    operator_id: Optional[StrictStr] = Field(
        default=None,
        description="The MCC/MNC of the sender's operator if known.",
    )
    sent_at: Optional[datetime] = Field(
        default=None,
        description="When the message left the originating device. Only available if provided by operator. Formatted as ISO-8601: YYYY-MM-DDThh:mm:ss.SSSZ.",
    )

