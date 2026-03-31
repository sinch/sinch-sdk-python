from typing import Optional
from pydantic import Field, StrictInt, conlist
from sinch.domains.sms.models.v1.shared import DryRunPerRecipientDetails
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)


class DryRunResponse(BaseModelConfigurationResponse):
    number_of_recipients: StrictInt = Field(
        default=..., description="The number of recipients in the batch"
    )
    number_of_messages: StrictInt = Field(
        default=...,
        description="The total number of SMS message parts to be sent in the batch",
    )
    per_recipient: Optional[conlist(DryRunPerRecipientDetails)] = None
