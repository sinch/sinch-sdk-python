from typing import Optional
from pydantic import Field
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.payment.dynamic_pix import (
    DynamicPix,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.payment.payment_link import (
    PaymentLink,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.payment.boleto import (
    Boleto,
)
from sinch.domains.conversation.models.v1.messages.internal.base import (
    BaseModelConfigurationResponse,
)


class PaymentSettings(BaseModelConfigurationResponse):
    dynamic_pix: Optional[DynamicPix] = Field(
        default=None, description="The dynamic Pix payment settings."
    )
    payment_link: Optional[PaymentLink] = Field(
        default=None, description="The payment link payment settings."
    )
    boleto: Optional[Boleto] = Field(
        default=None, description="The Boleto payment settings."
    )
