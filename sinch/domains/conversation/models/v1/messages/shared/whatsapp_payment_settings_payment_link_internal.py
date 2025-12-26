from pydantic import Field
from sinch.domains.conversation.models.v1.messages.shared.payment_link_internal import (
    PaymentLinkInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class WhatsAppPaymentSettingsPaymentLinkInternal(
    BaseModelConfigurationResponse
):
    payment_link: PaymentLinkInternal = Field(
        ..., description="The payment link payment settings."
    )
