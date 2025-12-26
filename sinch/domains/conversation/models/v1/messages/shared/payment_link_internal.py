from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class PaymentLinkInternal(BaseModelConfigurationResponse):
    uri: StrictStr = Field(
        ..., description="The payment link to be used by the buyer to pay."
    )
