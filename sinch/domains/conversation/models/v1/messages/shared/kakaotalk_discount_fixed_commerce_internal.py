from typing import Literal
from pydantic import Field, StrictInt
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_regular_price_commerce_internal import (
    KakaoTalkRegularPriceCommerceInternal,
)


class KakaoTalkDiscountFixedCommerceInternal(
    KakaoTalkRegularPriceCommerceInternal
):
    type: Literal["FIXED_DISCOUNT_COMMERCE"] = Field(
        "FIXED_DISCOUNT_COMMERCE", description="Commerce with fixed discount"
    )
    discount_price: StrictInt = Field(
        ..., description="Discounted price of the product"
    )
    discount_fixed: StrictInt = Field(..., description="Fixed discount")
