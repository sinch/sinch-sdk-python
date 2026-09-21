from typing import Optional
from pydantic import Field, StrictBool, StrictInt
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class DeliveryReportBasedFallback(BaseModelConfiguration):
    enabled: Optional[StrictBool] = Field(
        default=None,
        description="A flag specifying whether this app has enabled fallback message delivery upon no positive delivery report. This feature is applicable only to messages which are sent to a recipient with more than one channel identity. Identities must be defined on channels which support at least the 'DELIVERED' message state. **Please note that this functionality requires payment.**",
    )
    delivery_report_waiting_time: Optional[StrictInt] = Field(
        default=None,
        description="The time, in seconds, after which a message without a positive delivery report will fallback to the next channel. Minimum value is 10 and maximum value is 259200.",
    )
