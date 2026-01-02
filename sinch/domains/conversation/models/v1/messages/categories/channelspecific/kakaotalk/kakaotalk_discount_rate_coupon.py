from typing import Literal
from pydantic import Field, StrictInt
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.kakaotalk_coupon import (
    KakaoTalkCoupon,
)


class KakaoTalkDiscountRateCoupon(KakaoTalkCoupon):
    type: Literal["PERCENTAGE_DISCOUNT_COUPON"] = Field(
        "PERCENTAGE_DISCOUNT_COUPON", description="Percentage discount coupon"
    )
    discount_rate: StrictInt = Field(..., description="Discount rate (%)")
