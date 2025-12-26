from pydantic import Field
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_channel_specific_message_internal import (
    KakaoTalkChannelSpecificMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_carousel_internal import (
    KakaoTalkCarouselInternal,
)


class KakaoTalkCarouselCommerceChannelSpecificMessageInternal(
    KakaoTalkChannelSpecificMessageInternal
):
    carousel: KakaoTalkCarouselInternal = Field(
        ..., description="Carousel content"
    )
