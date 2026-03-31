from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.payment import (
    PaymentOrderStatusOrder,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfiguration,
)


class PaymentOrderStatusContent(BaseModelConfiguration):
    reference_id: StrictStr = Field(
        ..., description="Unique ID used to query the current payment status."
    )
    order: PaymentOrderStatusOrder = Field(
        ..., description="The payment order."
    )
