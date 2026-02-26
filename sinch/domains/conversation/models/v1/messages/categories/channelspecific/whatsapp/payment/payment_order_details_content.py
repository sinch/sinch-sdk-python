from typing import Optional
from pydantic import Field, StrictStr, StrictInt, conlist
from sinch.domains.conversation.models.v1.messages.types import (
    PaymentOrderType,
    PaymentOrderGoodsType,
)
from sinch.domains.conversation.models.v1.messages.response.types.whatsapp_payment_button import (
    WhatsAppPaymentButton,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.payment import (
    PaymentOrder,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class PaymentOrderDetailsContent(BaseModelConfiguration):
    type: PaymentOrderType = Field(
        ...,
        description="The country/currency associated with the payment message.",
    )
    reference_id: StrictStr = Field(..., description="Unique reference ID.")
    type_of_goods: PaymentOrderGoodsType = Field(
        ..., description="The type of good associated with this order."
    )
    total_amount_value: StrictInt = Field(
        ...,
        description="Integer representing the total amount of the transaction.",
    )
    order: PaymentOrder = Field(..., description="The payment order.")
    payment_buttons: Optional[conlist(WhatsAppPaymentButton)] = Field(
        default=None,
        description="Array of payment buttons (1 to 2 items).",
    )
