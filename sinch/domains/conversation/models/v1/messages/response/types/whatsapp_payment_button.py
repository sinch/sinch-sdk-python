from typing import Union
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.buttons.whatsapp_payment_settings_button_pix import (
    WhatsAppPaymentSettingsPixButton,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.buttons.whatsapp_payment_settings_button_payment_link import (
    WhatsAppPaymentSettingsPaymentLinkButton,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.buttons.whatsapp_payment_settings_button_boleto import (
    WhatsAppPaymentSettingsBoletoButton,
)

WhatsAppPaymentButton = Union[
    WhatsAppPaymentSettingsPixButton,
    WhatsAppPaymentSettingsPaymentLinkButton,
    WhatsAppPaymentSettingsBoletoButton,
]
