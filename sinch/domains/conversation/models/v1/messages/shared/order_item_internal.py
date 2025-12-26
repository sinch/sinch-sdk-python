from typing import Optional
from pydantic import Field, StrictStr, StrictInt
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class OrderItemInternal(BaseModelConfigurationResponse):
    retailer_id: StrictStr = Field(
        ..., description="Unique ID of the retailer."
    )
    name: StrictStr = Field(
        ..., description="Item's name as displayed to the user."
    )
    amount_value: StrictInt = Field(..., description="Price per item.")
    quantity: StrictInt = Field(
        ..., description="Number of items in this order."
    )
    sale_amount_value: Optional[StrictInt] = Field(
        default=None, description="Discounted price per item."
    )
