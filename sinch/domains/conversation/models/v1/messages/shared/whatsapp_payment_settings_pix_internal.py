from pydantic import Field
from sinch.domains.conversation.models.v1.messages.shared.dynamic_pix_internal import (
    DynamicPixInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class WhatsAppPaymentSettingsPixInternal(BaseModelConfigurationResponse):
    dynamic_pix: DynamicPixInternal = Field(
        ..., description="The dynamic Pix payment settings."
    )
