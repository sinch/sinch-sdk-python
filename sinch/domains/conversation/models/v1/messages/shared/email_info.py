from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class EmailInfo(BaseModelConfigurationResponse):
    email_address: StrictStr = Field(default=..., description="Email address.")
    type: Optional[StrictStr] = Field(
        default=None, description="Email address type. e.g. WORK or HOME."
    )
