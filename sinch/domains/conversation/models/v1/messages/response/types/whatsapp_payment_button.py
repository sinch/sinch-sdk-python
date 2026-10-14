from typing import Annotated, Union
from sinch.core.models.internal.unions import ResolveUnion
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.buttons.whatsapp_payment_settings_pix_button import (
    WhatsAppPaymentSettingsPixButton,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.buttons.whatsapp_payment_settings_payment_link_button import (
    WhatsAppPaymentSettingsPaymentLinkButton,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.buttons.whatsapp_payment_settings_boleto_button import (
    WhatsAppPaymentSettingsBoletoButton,
)

WhatsAppPaymentButton = Annotated[
    Union[
        WhatsAppPaymentSettingsPixButton,
        WhatsAppPaymentSettingsPaymentLinkButton,
        WhatsAppPaymentSettingsBoletoButton,
    ],
    ResolveUnion(discriminator="type", discriminator_strict=False),
]
