from typing import Optional
from pydantic import Field, StrictStr
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class KakaoTalkCouponInternal(BaseModelConfigurationResponse):
    description: Optional[StrictStr] = Field(
        default=None, description="Coupon description"
    )
    link_mo: Optional[StrictStr] = Field(
        default=None, description="Coupon URL opened on a mobile device"
    )
    link_pc: Optional[StrictStr] = Field(
        default=None, description="Coupon URL opened on a desktop device"
    )
    scheme_android: Optional[StrictStr] = Field(
        default=None,
        description="Channel coupon URL (format: `alimtalk=coupon://...`)",
    )
    scheme_ios: Optional[StrictStr] = Field(
        default=None,
        description="Channel coupon URL (format: `alimtalk=coupon://...`)",
    )
