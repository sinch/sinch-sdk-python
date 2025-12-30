from pydantic import Field
from sinch.domains.conversation.models.v1.messages.response.shared.payment_link import (
    PaymentLink,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class WhatsAppPaymentSettingsPaymentLink(BaseModelConfigurationResponse):
    payment_link: PaymentLink = Field(
        ..., description="The payment link payment settings."
    )
