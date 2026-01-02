from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class CallMessage(BaseModelConfigurationResponse):
    phone_number: StrictStr = Field(
        default=..., description="Phone number in E.164 with leading +."
    )
    title: StrictStr = Field(
        default=...,
        description="Title shown close to the phone number. The title is clickable in some cases.",
    )
