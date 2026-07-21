from typing import Optional
from pydantic import Field, StrictInt
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class MessageRetrySettings(BaseModelConfiguration):
    retry_duration: Optional[StrictInt] = Field(
        default=None,
        description="The maximum duration, in seconds, during which the system will retry sending a message in the event of a temporary processing failure. Time is counted after the first message processing failure. At least one retry is guaranteed. Subsequent retry instances are randomized with exponential backoff. If the next retry timestamp exceeds the configured time, one final retry will be performed on the cut-off time. The valid values for this field are [30 - 3600].",
    )
