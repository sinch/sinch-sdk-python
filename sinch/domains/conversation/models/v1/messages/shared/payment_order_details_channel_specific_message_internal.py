from pydantic import Field
from sinch.domains.conversation.models.v1.messages.shared.channel_specific_common_props import (
    ChannelSpecificCommonProps,
)
from sinch.domains.conversation.models.v1.messages.shared.payment_order_details_content_internal import (
    PaymentOrderDetailsContentInternal,
)


class PaymentOrderDetailsChannelSpecificMessageInternal(
    ChannelSpecificCommonProps
):
    payment: PaymentOrderDetailsContentInternal = Field(
        ..., description="The payment order details content."
    )
