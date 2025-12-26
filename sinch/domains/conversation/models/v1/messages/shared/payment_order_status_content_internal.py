from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.shared.payment_order_status_order_internal import (
    PaymentOrderStatusOrderInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class PaymentOrderStatusContentInternal(BaseModelConfigurationResponse):
    reference_id: StrictStr = Field(
        ..., description="Unique ID used to query the current payment status."
    )
    order: PaymentOrderStatusOrderInternal = Field(
        ..., description="The payment order."
    )
