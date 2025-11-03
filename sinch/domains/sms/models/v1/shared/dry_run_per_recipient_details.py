from pydantic import Field, StrictInt, StrictStr
from sinch.domains.sms.models.v1.internal.base import (
    BaseModelConfigurationResponse,
)


class DryRunPerRecipientDetails(BaseModelConfigurationResponse):
    recipient: StrictStr = Field(
        default=...,
        description="Sender number.    Required if Automatic Default Originator not configured.",
    )
    body: StrictStr = Field(...)
    number_of_parts: StrictInt = Field(...)
    encoding: StrictStr = Field(...)
