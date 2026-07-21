from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class AppleBusinessChatCredentials(BaseModelConfiguration):
    business_chat_account_id: StrictStr = Field(
        default=...,
        description="The ID that identifies a Business Chat Account (BCA).",
    )
    merchant_id: Optional[StrictStr] = Field(
        default=None,
        description="Merchant ID, required if our client wants to use Apple Pay.",
    )
    apple_pay_certificate_reference: Optional[StrictStr] = Field(
        default=None,
        description="Certificate reference, required if our client wants to use Apple Pay.",
    )
    apple_pay_certificate_password: Optional[StrictStr] = Field(
        default=None,
        description="Certificate password, required if our client wants to use Apple Pay.",
    )
