from typing import Literal
from pydantic import Field, StrictInt
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_regular_price_commerce import (
    KakaoTalkRegularPriceCommerce,
)


class KakaoTalkDiscountFixedCommerce(KakaoTalkRegularPriceCommerce):
    type: Literal["FIXED_DISCOUNT_COMMERCE"] = Field(
        "FIXED_DISCOUNT_COMMERCE", description="Commerce with fixed discount"
    )
    discount_price: StrictInt = Field(
        ..., description="Discounted price of the product"
    )
    discount_fixed: StrictInt = Field(..., description="Fixed discount")
