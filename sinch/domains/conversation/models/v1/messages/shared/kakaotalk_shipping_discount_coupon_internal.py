from typing import Literal
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_coupon_internal import (
    KakaoTalkCouponInternal,
)


class KakaoTalkShippingDiscountCouponInternal(KakaoTalkCouponInternal):
    type: Literal["SHIPPING_DISCOUNT_COUPON"] = Field(
        "SHIPPING_DISCOUNT_COUPON", description="Shipping discount coupon"
    )
