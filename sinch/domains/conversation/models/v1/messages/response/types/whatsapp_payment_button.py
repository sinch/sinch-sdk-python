from typing import Union
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.buttons.whatsapp_payment_settings_pix_button import (
    WhatsAppPaymentSettingsPixButton,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.buttons.whatsapp_payment_settings_payment_link_button import (
    WhatsAppPaymentSettingsPaymentLinkButton,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.buttons.whatsapp_payment_settings_boleto_button import (
    WhatsAppPaymentSettingsBoletoButton,
)

WhatsAppPaymentButton = Union[
    WhatsAppPaymentSettingsPixButton,
    WhatsAppPaymentSettingsPaymentLinkButton,
    WhatsAppPaymentSettingsBoletoButton,
]
