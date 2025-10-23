from typing import Optional
from pydantic import Field, StrictInt, StrictStr, conlist
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)


class MessageDeliveryStatus(BaseModelConfigurationResponse):
    code: StrictInt = Field(
        default=..., description="The delivery receipt error code."
    )
    count: StrictInt = Field(
        default=..., description="The number of messages with this status."
    )
    recipients: Optional[conlist(StrictStr)] = Field(
        default=None,
        description="List of phone numbers (MSISDNs) with this status. Only present in full reports.",
    )
    status: StrictStr = Field(default=..., description="The delivery status.")
