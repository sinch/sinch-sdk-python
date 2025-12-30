from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.response.shared.payment_order_status_order import (
    PaymentOrderStatusOrder,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class PaymentOrderStatusContent(BaseModelConfigurationResponse):
    reference_id: StrictStr = Field(
        ..., description="Unique ID used to query the current payment status."
    )
    order: PaymentOrderStatusOrder = Field(
        ..., description="The payment order."
    )
