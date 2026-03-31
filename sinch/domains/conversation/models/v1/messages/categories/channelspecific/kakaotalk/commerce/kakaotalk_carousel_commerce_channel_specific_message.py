from pydantic import Field
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.commerce import (
    KakaoTalkCarousel,
    KakaoTalkChannelSpecificMessage,
)


class KakaoTalkCarouselCommerceChannelSpecificMessage(
    KakaoTalkChannelSpecificMessage
):
    carousel: KakaoTalkCarousel = Field(..., description="Carousel content")
