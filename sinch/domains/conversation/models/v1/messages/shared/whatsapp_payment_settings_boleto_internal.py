from pydantic import Field
from sinch.domains.conversation.models.v1.messages.shared.boleto_internal import (
    BoletoInternal,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class WhatsAppPaymentSettingsBoletoInternal(BaseModelConfigurationResponse):
    boleto: BoletoInternal = Field(
        ..., description="The Boleto payment settings."
    )
