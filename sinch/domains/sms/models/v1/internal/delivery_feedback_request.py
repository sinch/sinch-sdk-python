from pydantic import Field, StrictStr, conlist
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationRequest,
)


class DeliveryFeedbackRequest(BaseModelConfigurationRequest):
    batch_id: StrictStr = Field(
        default=...,
        description="The unique identifier of the batch message for which delivery feedback is being provided.",
    )
    recipients: conlist(StrictStr) = Field(
        default=...,
        description="A list of phone numbers (MSISDNs) that have successfully received the message. The key is required, however, the value can be an empty array (`[]`) for *a batch*. If the feedback was enabled for *a group*, at least one phone number is required.",
    )
