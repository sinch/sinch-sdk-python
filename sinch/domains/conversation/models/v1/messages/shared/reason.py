from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.types.reason_code_type import (
    ReasonCodeType,
)
from sinch.domains.conversation.models.v1.messages.types.reason_sub_code_type import (
    ReasonSubCodeType,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class Reason(BaseModelConfigurationResponse):
    code: Optional[ReasonCodeType] = None
    description: Optional[StrictStr] = Field(
        default=None, description="A textual description of the reason."
    )
    sub_code: Optional[ReasonSubCodeType] = None
    channel_code: Optional[StrictStr] = Field(
        default=None,
        description="Error code forwarded directly from the channel. Useful in case of unmapped or channel specific errors. Currently only supported on the WhatsApp channel.",
    )
