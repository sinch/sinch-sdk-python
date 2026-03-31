from typing import Literal
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class WhatsAppPaymentSettingsPaymentLinkButton(BaseModelConfiguration):
    type: Literal["payment_link"] = Field(
        ...,
        description="The payment link button identifier",
    )
    uri: StrictStr = Field(
        ..., description="The payment link to be used by the buyer to pay."
    )
