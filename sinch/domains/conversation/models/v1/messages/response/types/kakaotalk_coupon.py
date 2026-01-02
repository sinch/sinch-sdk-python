from typing import Annotated, Union
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.kakaotalk_fixed_discount_coupon import (
    KakaoTalkFixedDiscountCoupon,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.kakaotalk_discount_rate_coupon import (
    KakaoTalkDiscountRateCoupon,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.kakaotalk_shipping_discount_coupon import (
    KakaoTalkShippingDiscountCoupon,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.kakaotalk_free_coupon import (
    KakaoTalkFreeCoupon,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.kakaotalk_up_coupon import (
    KakaoTalkUpCoupon,
)


_KakaoTalkCouponUnion = Union[
    KakaoTalkFixedDiscountCoupon,
    KakaoTalkDiscountRateCoupon,
    KakaoTalkShippingDiscountCoupon,
    KakaoTalkFreeCoupon,
    KakaoTalkUpCoupon,
]

KakaoTalkCoupon = Annotated[_KakaoTalkCouponUnion, Field(discriminator="type")]
