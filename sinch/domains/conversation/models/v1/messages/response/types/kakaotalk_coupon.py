from sinch.core.models.internal.unions import ResolveUnion
from typing import Annotated, Union
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.coupons.kakaotalk_fixed_discount_coupon import (
    KakaoTalkFixedDiscountCoupon,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.coupons.kakaotalk_discount_rate_coupon import (
    KakaoTalkDiscountRateCoupon,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.coupons.kakaotalk_shipping_discount_coupon import (
    KakaoTalkShippingDiscountCoupon,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.coupons.kakaotalk_free_coupon import (
    KakaoTalkFreeCoupon,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.coupons.kakaotalk_up_coupon import (
    KakaoTalkUpCoupon,
)


_KakaoTalkCouponUnion = Union[
    KakaoTalkFixedDiscountCoupon,
    KakaoTalkDiscountRateCoupon,
    KakaoTalkShippingDiscountCoupon,
    KakaoTalkFreeCoupon,
    KakaoTalkUpCoupon,
]

KakaoTalkCoupon = Annotated[
    Union[
        KakaoTalkFixedDiscountCoupon,
        KakaoTalkDiscountRateCoupon,
        KakaoTalkShippingDiscountCoupon,
        KakaoTalkFreeCoupon,
        KakaoTalkUpCoupon,
    ],
    ResolveUnion(discriminator="type"),
]
