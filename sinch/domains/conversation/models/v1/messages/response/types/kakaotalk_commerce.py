from typing import Union
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_regular_price_commerce import (
    KakaoTalkRegularPriceCommerce,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_discount_fixed_commerce import (
    KakaoTalkDiscountFixedCommerce,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_discount_rate_commerce import (
    KakaoTalkDiscountRateCommerce,
)


KakaoTalkCommerce = Union[
    KakaoTalkRegularPriceCommerce,
    KakaoTalkDiscountFixedCommerce,
    KakaoTalkDiscountRateCommerce,
]
