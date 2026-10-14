from typing import Annotated, Union
from sinch.core.models.internal.unions import ResolveUnion
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.commerce.kakaotalk_regular_price_commerce import (
    KakaoTalkRegularPriceCommerce,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.commerce.kakaotalk_discount_fixed_commerce import (
    KakaoTalkDiscountFixedCommerce,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.commerce.kakaotalk_discount_rate_commerce import (
    KakaoTalkDiscountRateCommerce,
)


KakaoTalkCommerce = Annotated[
    Union[
        KakaoTalkRegularPriceCommerce,
        KakaoTalkDiscountFixedCommerce,
        KakaoTalkDiscountRateCommerce,
    ],
    ResolveUnion(discriminator="type", discriminator_strict=False),
]
