from pydantic import Field
from sinch.domains.conversation.models.v1.messages.response.shared.boleto import (
    Boleto,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class WhatsAppPaymentSettingsBoleto(BaseModelConfigurationResponse):
    boleto: Boleto = Field(..., description="The Boleto payment settings.")
