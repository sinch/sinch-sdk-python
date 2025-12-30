from pydantic import Field
from sinch.domains.conversation.models.v1.messages.shared.whatsapp_common_props import (
    WhatsAppCommonProps,
)
from sinch.domains.conversation.models.v1.messages.response.shared.payment_order_details_content import (
    PaymentOrderDetailsContent,
)


class PaymentOrderDetailsChannelSpecificMessage(WhatsAppCommonProps):
    payment: PaymentOrderDetailsContent = Field(
        ..., description="The payment order details content."
    )
