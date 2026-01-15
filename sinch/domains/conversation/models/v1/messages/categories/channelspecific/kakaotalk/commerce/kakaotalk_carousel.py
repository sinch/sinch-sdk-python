from typing import Optional
from pydantic import Field, conlist
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.commerce import (
    KakaoTalkCarouselHead,
    KakaoTalkCarouselTail,
    KakaoTalkCommerceMessage,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class KakaoTalkCarousel(BaseModelConfigurationResponse):
    head: Optional[KakaoTalkCarouselHead] = Field(
        default=None, description="Carousel introduction"
    )
    list: conlist(KakaoTalkCommerceMessage) = Field(
        ..., description="List of carousel cards"
    )
    tail: Optional[KakaoTalkCarouselTail] = Field(
        default=None, description="More button"
    )
