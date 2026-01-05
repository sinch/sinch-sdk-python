from pydantic import Field
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.whatsapp_common_props import (
    WhatsAppCommonProps,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.payment.payment_order_status_content import (
    PaymentOrderStatusContent,
)


class PaymentOrderStatusChannelSpecificMessage(WhatsAppCommonProps):
    payment: PaymentOrderStatusContent = Field(
        ..., description="The payment order status message content"
    )
