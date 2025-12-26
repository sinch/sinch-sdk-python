from typing import Literal
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_coupon_internal import (
    KakaoTalkCouponInternal,
)


class KakaoTalkFreeCouponInternal(KakaoTalkCouponInternal):
    type: Literal["FREE_COUPON"] = Field(
        "FREE_COUPON", description="Free coupon"
    )
    title: StrictStr = Field(..., description="Coupon title")
