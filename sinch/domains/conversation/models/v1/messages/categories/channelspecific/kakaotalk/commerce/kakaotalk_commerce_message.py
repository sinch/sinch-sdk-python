from typing import Optional
from pydantic import Field, StrictStr, conlist
from sinch.domains.conversation.models.v1.messages.response.types.kakaotalk_button import (
    KakaoTalkButton,
)
from sinch.domains.conversation.models.v1.messages.response.types.kakaotalk_commerce import (
    KakaoTalkCommerce,
)
from sinch.domains.conversation.models.v1.messages.response.types.kakaotalk_coupon import (
    KakaoTalkCoupon,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.commerce import (
    KakaoTalkCommerceImage,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class KakaoTalkCommerceMessage(BaseModelConfigurationResponse):
    buttons: conlist(KakaoTalkButton) = Field(..., description="Buttons list")
    additional_content: Optional[StrictStr] = Field(
        default=None, description="Additional information", max_length=34
    )
    image: KakaoTalkCommerceImage = Field(..., description="Product image")
    commerce: KakaoTalkCommerce = Field(..., description="Product information")
    coupon: Optional[KakaoTalkCoupon] = Field(
        default=None, description="Discount coupon"
    )
