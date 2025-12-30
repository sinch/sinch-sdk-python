from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.types.payment_order_status_type import (
    PaymentOrderStatusType,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class PaymentOrderStatusOrder(BaseModelConfigurationResponse):
    status: PaymentOrderStatusType = Field(
        ..., description="The new payment message status."
    )
    description: Optional[StrictStr] = Field(
        default=None,
        description="The description of payment message status update (120 characters maximum).",
    )
