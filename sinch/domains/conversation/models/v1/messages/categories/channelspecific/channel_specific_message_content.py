from typing import Annotated, Union
from sinch.core.models.internal.unions import ResolveUnion

from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.commerce.kakaotalk_carousel_commerce_channel_specific_message import (
    KakaoTalkCarouselCommerceChannelSpecificMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.kakaotalk.commerce.kakaotalk_commerce_channel_specific_message import (
    KakaoTalkCommerceChannelSpecificMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.line.line_notification_message_template_message import (
    LineNotificationMessageTemplateMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.flows.flow_channel_specific_message import (
    FlowChannelSpecificMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.payment.payment_order_details_channel_specific_message import (
    PaymentOrderDetailsChannelSpecificMessage,
)
from sinch.domains.conversation.models.v1.messages.categories.channelspecific.whatsapp.payment.payment_order_status_channel_specific_message import (
    PaymentOrderStatusChannelSpecificMessage,
)

ChannelSpecificMessageContent = Annotated[
    Union[
        FlowChannelSpecificMessage,
        PaymentOrderDetailsChannelSpecificMessage,
        PaymentOrderStatusChannelSpecificMessage,
        KakaoTalkCommerceChannelSpecificMessage,
        KakaoTalkCarouselCommerceChannelSpecificMessage,
        LineNotificationMessageTemplateMessage,
    ],
    ResolveUnion(),
]
