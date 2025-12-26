from typing import Optional
from pydantic import Field, StrictStr, conlist
from sinch.domains.conversation.models.v1.messages.types.kakaotalk_button_internal import (
    KakaoTalkButtonInternalUnion,
)
from sinch.domains.conversation.models.v1.messages.types.kakaotalk_commerce_internal import (
    KakaoTalkCommerceInternal,
)
from sinch.domains.conversation.models.v1.messages.types.kakaotalk_coupon_internal import (
    KakaoTalkCouponInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_commerce_image_internal import (
    KakaoTalkCommerceImageInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class KakaoTalkCommerceMessageInternal(BaseModelConfigurationResponse):
    buttons: conlist(KakaoTalkButtonInternalUnion) = Field(
        ..., description="Buttons list"
    )
    additional_content: Optional[StrictStr] = Field(
        default=None, description="Additional information", max_length=34
    )
    image: KakaoTalkCommerceImageInternal = Field(
        ..., description="Product image"
    )
    commerce: KakaoTalkCommerceInternal = Field(
        ..., description="Product information"
    )
    coupon: Optional[KakaoTalkCouponInternal] = Field(
        default=None, description="Discount coupon"
    )
