from pydantic import Field
from sinch.domains.conversation.models.v1.messages.response.shared.dynamic_pix import (
    DynamicPix,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class WhatsAppPaymentSettingsPix(BaseModelConfigurationResponse):
    dynamic_pix: DynamicPix = Field(
        ..., description="The dynamic Pix payment settings."
    )
