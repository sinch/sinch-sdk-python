from pydantic import Field
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_channel_specific_message import (
    KakaoTalkChannelSpecificMessage,
)
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_carousel import (
    KakaoTalkCarousel,
)


class KakaoTalkCarouselCommerceChannelSpecificMessage(
    KakaoTalkChannelSpecificMessage
):
    carousel: KakaoTalkCarousel = Field(..., description="Carousel content")
