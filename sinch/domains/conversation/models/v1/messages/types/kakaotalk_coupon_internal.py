from typing import Union
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_fixed_discount_coupon_internal import (
    KakaoTalkFixedDiscountCouponInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_discount_rate_coupon_internal import (
    KakaoTalkDiscountRateCouponInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_shipping_discount_coupon_internal import (
    KakaoTalkShippingDiscountCouponInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_free_coupon_internal import (
    KakaoTalkFreeCouponInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_up_coupon_internal import (
    KakaoTalkUpCouponInternal,
)


KakaoTalkCouponInternal = Union[
    KakaoTalkFixedDiscountCouponInternal,
    KakaoTalkDiscountRateCouponInternal,
    KakaoTalkShippingDiscountCouponInternal,
    KakaoTalkFreeCouponInternal,
    KakaoTalkUpCouponInternal,
]
