from typing import Literal
from pydantic import Field, StrictStr, StrictInt
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class KakaoTalkRegularPriceCommerce(BaseModelConfigurationResponse):
    type: Literal["REGULAR_PRICE_COMMERCE"] = Field(
        "REGULAR_PRICE_COMMERCE", description="Commerce with regular price"
    )
    title: StrictStr = Field(..., description="Product title")
    regular_price: StrictInt = Field(
        ..., description="Regular price of the product"
    )
