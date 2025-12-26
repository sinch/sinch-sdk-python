from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.shared.reason_code import (
    ReasonCode,
)
from sinch.domains.conversation.models.v1.messages.shared.reason_sub_code import (
    ReasonSubCode,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class Reason(BaseModelConfigurationResponse):
    code: Optional[ReasonCode] = None
    description: Optional[StrictStr] = Field(
        default=None, description="A textual description of the reason."
    )
    sub_code: Optional[ReasonSubCode] = None
    channel_code: Optional[StrictStr] = Field(
        default=None,
        description="Error code forwarded directly from the channel. Useful in case of unmapped or channel specific errors. Currently only supported on the WhatsApp channel.",
    )
