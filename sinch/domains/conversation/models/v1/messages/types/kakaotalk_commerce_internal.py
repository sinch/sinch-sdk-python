from typing import Union
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_regular_price_commerce_internal import (
    KakaoTalkRegularPriceCommerceInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_discount_fixed_commerce_internal import (
    KakaoTalkDiscountFixedCommerceInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_discount_rate_commerce_internal import (
    KakaoTalkDiscountRateCommerceInternal,
)


KakaoTalkCommerceInternal = Union[
    KakaoTalkRegularPriceCommerceInternal,
    KakaoTalkDiscountFixedCommerceInternal,
    KakaoTalkDiscountRateCommerceInternal,
]
