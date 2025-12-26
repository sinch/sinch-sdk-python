from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class PhoneNumberInfo(BaseModelConfigurationResponse):
    phone_number: StrictStr = Field(
        default=..., description="Phone number with country code included."
    )
    type: Optional[StrictStr] = Field(
        default=None, description="Phone number type, e.g. WORK or HOME."
    )
