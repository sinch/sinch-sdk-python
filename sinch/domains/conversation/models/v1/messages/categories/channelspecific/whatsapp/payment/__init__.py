from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.payment.order_item import (
    OrderItem,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.payment.payment_order_status_order import (
    PaymentOrderStatusOrder,
)


def __getattr__(name: str):
    if name == "PaymentOrder":
        from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.payment.payment_order import (
            PaymentOrder,
        )

        return PaymentOrder
    if name == "PaymentOrderDetailsContent":
        from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.payment.payment_order_details_content import (
            PaymentOrderDetailsContent,
        )

        return PaymentOrderDetailsContent
    if name == "PaymentOrderStatusContent":
        from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.payment.payment_order_status_content import (
            PaymentOrderStatusContent,
        )

        return PaymentOrderStatusContent
    if name == "PaymentOrderDetailsChannelSpecificMessage":
        from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.payment.payment_order_details_channel_specific_message import (
            PaymentOrderDetailsChannelSpecificMessage,
        )

        return PaymentOrderDetailsChannelSpecificMessage
    if name == "PaymentOrderStatusChannelSpecificMessage":
        from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.payment.payment_order_status_channel_specific_message import (
            PaymentOrderStatusChannelSpecificMessage,
        )

        return PaymentOrderStatusChannelSpecificMessage
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "OrderItem",
    "PaymentOrderStatusOrder",
    "PaymentOrder",
    "PaymentOrderDetailsContent",
    "PaymentOrderStatusContent",
    "PaymentOrderDetailsChannelSpecificMessage",
    "PaymentOrderStatusChannelSpecificMessage",
]
