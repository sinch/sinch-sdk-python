from typing import Optional, Union
from pydantic import Field, StrictFloat, StrictInt, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class ProductItem(BaseModelConfigurationResponse):
    id: StrictStr = Field(
        default=..., description="Required parameter. The ID for the product."
    )
    marketplace: StrictStr = Field(
        default=...,
        description="Required parameter. The marketplace to which the product belongs.",
    )
    quantity: Optional[StrictInt] = Field(
        default=None,
        description="Output only. The quantity of the chosen product.",
    )
    item_price: Optional[Union[StrictFloat, StrictInt]] = Field(
        default=None,
        description="Output only. The price for one unit of the chosen product.",
    )
    currency: Optional[StrictStr] = Field(
        default=None,
        description="Output only. The currency of the item_price.",
    )
