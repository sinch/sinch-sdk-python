from typing import Optional
from pydantic import Field, StrictStr, conlist
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.commerce import (
    KakaoTalkChannelSpecificMessage,
    KakaoTalkCommerceImage,
)
from sinch.domains.conversation.models.v1.messages.response.types.kakaotalk_button import (
    KakaoTalkButton,
)
from sinch.domains.conversation.models.v1.messages.response.types.kakaotalk_commerce import (
    KakaoTalkCommerce,
)
from sinch.domains.conversation.models.v1.messages.response.types.kakaotalk_coupon import (
    KakaoTalkCoupon,
)


class KakaoTalkCommerceChannelSpecificMessage(KakaoTalkChannelSpecificMessage):
    buttons: conlist(KakaoTalkButton) = Field(..., description="Buttons list")
    additional_content: Optional[StrictStr] = Field(
        default=None, description="Additional information"
    )
    image: KakaoTalkCommerceImage = Field(..., description="Product image")
    commerce: KakaoTalkCommerce = Field(..., description="Product information")
    coupon: Optional[KakaoTalkCoupon] = Field(
        default=None, description="Discount coupon"
    )
