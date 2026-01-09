from datetime import datetime
from typing import Optional
from pydantic import Field, StrictStr, StrictInt, conlist
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.payment.order_item import (
    OrderItem,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class PaymentOrder(BaseModelConfigurationResponse):
    items: conlist(OrderItem) = Field(
        ..., description="The items list for this order."
    )
    subtotal_value: StrictInt = Field(
        ...,
        description="Value representing the subtotal amount of this order.",
    )
    tax_value: StrictInt = Field(
        ..., description="Value representing the tax amount for this order."
    )
    catalog_id: Optional[StrictStr] = Field(
        default=None,
        description="Unique ID of the Facebook catalog being used by the business.",
    )
    expiration_time: Optional[datetime] = Field(
        default=None,
        description="UTC timestamp indicating when the order should expire.",
    )
    expiration_description: Optional[StrictStr] = Field(
        default=None, description="Description of the expiration."
    )
    tax_description: Optional[StrictStr] = Field(
        default=None, description="Description of the tax for this order."
    )
    shipping_value: Optional[StrictInt] = Field(
        default=None,
        description="Value representing the shipping amount for this order.",
    )
    shipping_description: Optional[StrictStr] = Field(
        default=None, description="Shipping description for this order."
    )
    discount_value: Optional[StrictInt] = Field(
        default=None, description="Value of the discount for this order."
    )
    discount_description: Optional[StrictStr] = Field(
        default=None, description="Description of the discount for this order."
    )
    discount_program_name: Optional[StrictStr] = Field(
        default=None, description="Discount program name for this order."
    )
