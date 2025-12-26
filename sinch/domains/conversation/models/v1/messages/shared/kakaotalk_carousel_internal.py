from typing import Optional
from pydantic import Field, conlist
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_carousel_head_internal import (
    KakaoTalkCarouselHeadInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_carousel_tail_internal import (
    KakaoTalkCarouselTailInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_commerce_message_internal import (
    KakaoTalkCommerceMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class KakaoTalkCarouselInternal(BaseModelConfigurationResponse):
    head: Optional[KakaoTalkCarouselHeadInternal] = Field(
        default=None, description="Carousel introduction"
    )
    list: conlist(KakaoTalkCommerceMessageInternal) = Field(
        ..., description="List of carousel cards"
    )
    tail: Optional[KakaoTalkCarouselTailInternal] = Field(
        default=None, description="More button"
    )
