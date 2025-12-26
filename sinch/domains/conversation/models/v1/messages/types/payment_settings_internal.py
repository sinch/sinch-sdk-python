from typing import Union
from sinch.domains.conversation.models.v1.messages.shared.whatsapp_payment_settings_pix_internal import (
    WhatsAppPaymentSettingsPixInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.whatsapp_payment_settings_payment_link_internal import (
    WhatsAppPaymentSettingsPaymentLinkInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.whatsapp_payment_settings_boleto_internal import (
    WhatsAppPaymentSettingsBoletoInternal,
)


PaymentSettingsInternal = Union[
    WhatsAppPaymentSettingsPixInternal,
    WhatsAppPaymentSettingsPaymentLinkInternal,
    WhatsAppPaymentSettingsBoletoInternal,
]
