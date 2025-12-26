from typing import Literal
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_coupon_internal import (
    KakaoTalkCouponInternal,
)


class KakaoTalkUpCouponInternal(KakaoTalkCouponInternal):
    type: Literal["UP_COUPON"] = Field("UP_COUPON", description="UP coupon")
    title: StrictStr = Field(..., description="Coupon title")
