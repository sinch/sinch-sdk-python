from typing import Union
from sinch.domains.conversation.models.v1.messages.response.shared.whatsapp_payment_settings_pix import (
    WhatsAppPaymentSettingsPix,
)
from sinch.domains.conversation.models.v1.messages.response.shared.whatsapp_payment_settings_payment_link import (
    WhatsAppPaymentSettingsPaymentLink,
)
from sinch.domains.conversation.models.v1.messages.response.shared.whatsapp_payment_settings_boleto import (
    WhatsAppPaymentSettingsBoleto,
)


PaymentSettings = Union[
    WhatsAppPaymentSettingsPix,
    WhatsAppPaymentSettingsPaymentLink,
    WhatsAppPaymentSettingsBoleto,
]
