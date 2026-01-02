from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class Boleto(BaseModelConfigurationResponse):
    digitable_line: StrictStr = Field(
        ...,
        description="The Boleto digitable line which will be copied to the clipboard when the user taps the Boleto button.",
    )
