from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.commerce.kakaotalk_channel_specific_message import (
    KakaoTalkChannelSpecificMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.commerce.kakaotalk_commerce_image import (
    KakaoTalkCommerceImage,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.commerce.kakaotalk_carousel_head import (
    KakaoTalkCarouselHead,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.commerce.kakaotalk_carousel_tail import (
    KakaoTalkCarouselTail,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.commerce.kakaotalk_regular_price_commerce import (
    KakaoTalkRegularPriceCommerce,
)


def __getattr__(name: str):
    if name == "KakaoTalkCommerceMessage":
        from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.commerce.kakaotalk_commerce_message import (
            KakaoTalkCommerceMessage,
        )

        return KakaoTalkCommerceMessage
    if name == "KakaoTalkCarousel":
        from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.commerce.kakaotalk_carousel import (
            KakaoTalkCarousel,
        )

        return KakaoTalkCarousel
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "KakaoTalkChannelSpecificMessage",
    "KakaoTalkCommerceImage",
    "KakaoTalkCarouselHead",
    "KakaoTalkCarouselTail",
    "KakaoTalkRegularPriceCommerce",
    "KakaoTalkCommerceMessage",
    "KakaoTalkCarousel",
]
