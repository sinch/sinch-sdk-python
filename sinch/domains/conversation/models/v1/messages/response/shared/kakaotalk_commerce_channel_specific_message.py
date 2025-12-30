from typing import Optional
from pydantic import Field, StrictStr, conlist
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_channel_specific_message import (
    KakaoTalkChannelSpecificMessage,
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
from sinch.domains.conversation.models.v1.messages.response.shared.kakaotalk_commerce_image import (
    KakaoTalkCommerceImage,
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
