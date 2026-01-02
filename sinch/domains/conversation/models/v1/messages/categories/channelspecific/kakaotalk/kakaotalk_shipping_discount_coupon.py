from typing import Literal
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.kakaotalk_coupon import (
    KakaoTalkCoupon,
)


class KakaoTalkShippingDiscountCoupon(KakaoTalkCoupon):
    type: Literal["SHIPPING_DISCOUNT_COUPON"] = Field(
        "SHIPPING_DISCOUNT_COUPON", description="Shipping discount coupon"
    )
