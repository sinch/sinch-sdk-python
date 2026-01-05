from typing import Union
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.flows.flow_channel_specific_message import (
    FlowChannelSpecificMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.payment.payment_order_details_channel_specific_message import (
    PaymentOrderDetailsChannelSpecificMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.payment.payment_order_status_channel_specific_message import (
    PaymentOrderStatusChannelSpecificMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.kakaotalk_commerce_channel_specific_message import (
    KakaoTalkCommerceChannelSpecificMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.kakaotalk_carousel_commerce_channel_specific_message import (
    KakaoTalkCarouselCommerceChannelSpecificMessage,
)


ChannelSpecificMessageContent = Union[
    FlowChannelSpecificMessage,
    PaymentOrderDetailsChannelSpecificMessage,
    PaymentOrderStatusChannelSpecificMessage,
    KakaoTalkCommerceChannelSpecificMessage,
    KakaoTalkCarouselCommerceChannelSpecificMessage,
]
