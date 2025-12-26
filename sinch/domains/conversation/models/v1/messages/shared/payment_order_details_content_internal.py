from typing import Optional
from pydantic import Field, StrictStr, StrictInt
from sinch.domains.conversation.models.v1.messages.types.payment_order_type import (
    PaymentOrderType,
)
from sinch.domains.conversation.models.v1.messages.types.payment_order_goods_type import (
    PaymentOrderGoodsType,
)
from sinch.domains.conversation.models.v1.messages.types.payment_settings_internal import (
    PaymentSettingsInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.payment_order_internal import (
    PaymentOrderInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class PaymentOrderDetailsContentInternal(BaseModelConfigurationResponse):
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
    order: PaymentOrderInternal = Field(..., description="The payment order.")
    payment_settings: Optional[PaymentSettingsInternal] = None
