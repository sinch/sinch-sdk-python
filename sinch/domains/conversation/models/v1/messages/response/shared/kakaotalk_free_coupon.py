from typing import Literal
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_coupon import (
    KakaoTalkCoupon,
)


class KakaoTalkFreeCoupon(KakaoTalkCoupon):
    type: Literal["FREE_COUPON"] = Field(
        "FREE_COUPON", description="Free coupon"
    )
    title: StrictStr = Field(..., description="Coupon title")
