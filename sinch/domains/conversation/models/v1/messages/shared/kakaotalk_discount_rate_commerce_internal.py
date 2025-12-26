from typing import Literal
from pydantic import Field, StrictInt
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_regular_price_commerce_internal import (
    KakaoTalkRegularPriceCommerceInternal,
)


class KakaoTalkDiscountRateCommerceInternal(
    KakaoTalkRegularPriceCommerceInternal
):
    type: Literal["PERCENTAGE_DISCOUNT_COMMERCE"] = Field(
        "PERCENTAGE_DISCOUNT_COMMERCE",
        description="Commerce with percentage discount",
    )
    discount_price: StrictInt = Field(
        ..., description="Discounted price of the product"
    )
    discount_rate: StrictInt = Field(..., description="Discount rate (%)")
