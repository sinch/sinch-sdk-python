from pydantic import Field
from sinch.domains.conversation.models.v1.messages.shared.channel_specific_common_props import (
    ChannelSpecificCommonProps,
)
from sinch.domains.conversation.models.v1.messages.shared.payment_order_status_content_internal import (
    PaymentOrderStatusContentInternal,
)


class PaymentOrderStatusChannelSpecificMessageInternal(
    ChannelSpecificCommonProps
):
    payment: PaymentOrderStatusContentInternal = Field(
        ..., description="The payment order status message content"
    )
