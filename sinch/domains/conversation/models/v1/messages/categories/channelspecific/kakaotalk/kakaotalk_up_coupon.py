from typing import Literal
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.kakaotalk_coupon import (
    KakaoTalkCoupon,
)


class KakaoTalkUpCoupon(KakaoTalkCoupon):
    type: Literal["UP_COUPON"] = Field("UP_COUPON", description="UP coupon")
    title: StrictStr = Field(..., description="Coupon title")
