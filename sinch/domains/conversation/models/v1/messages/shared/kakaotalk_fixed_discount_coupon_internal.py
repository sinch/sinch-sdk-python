from typing import Literal
from pydantic import Field, StrictInt
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_coupon_internal import (
    KakaoTalkCouponInternal,
)


class KakaoTalkFixedDiscountCouponInternal(KakaoTalkCouponInternal):
    type: Literal["FIXED_DISCOUNT_COUPON"] = Field(
        "FIXED_DISCOUNT_COUPON", description="Fixed discount coupon"
    )
    discount_fixed: StrictInt = Field(..., description="Fixed discount")
