from pydantic import Field
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.whatsapp_common_props import (
    WhatsAppCommonProps,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.payment import (
    PaymentOrderDetailsContent,
)


class PaymentOrderDetailsChannelSpecificMessage(WhatsAppCommonProps):
    payment: PaymentOrderDetailsContent = Field(
        ..., description="The payment order details content."
    )
