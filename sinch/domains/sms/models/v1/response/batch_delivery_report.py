from typing import Optional
from pydantic import Field, StrictStr, conlist, conint
from sinch.domains.sms.models.v1.shared import MessageDeliveryStatus
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)


class BatchDeliveryReport(BaseModelConfigurationResponse):
    batch_id: StrictStr = Field(
        default=...,
        description="The ID of the batch this delivery report belongs to.",
    )
    client_reference: Optional[StrictStr] = Field(
        default=None,
        description="The client identifier of the batch this delivery report belongs to, if set when submitting batch.",
    )
    statuses: conlist(MessageDeliveryStatus) = Field(
        default=...,
        description="Array with status objects. Only status codes with at least one recipient will be listed.",
    )
    total_message_count: conint(strict=True, ge=0) = Field(
        default=..., description="The total number of messages in the batch."
    )
    type: StrictStr = Field(
        default=..., description="The delivery report type."
    )
