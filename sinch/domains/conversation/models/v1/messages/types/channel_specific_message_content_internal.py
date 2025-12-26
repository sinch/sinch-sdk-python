from typing import Union
from sinch.domains.conversation.models.v1.messages.shared.flow_channel_specific_message_internal import (
    FlowChannelSpecificMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.payment_order_details_channel_specific_message_internal import (
    PaymentOrderDetailsChannelSpecificMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.payment_order_status_channel_specific_message_internal import (
    PaymentOrderStatusChannelSpecificMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_commerce_channel_specific_message_internal import (
    KakaoTalkCommerceChannelSpecificMessageInternal,
)
from sinch.domains.conversation.models.v1.messages.shared.kakaotalk_carousel_commerce_channel_specific_message_internal import (
    KakaoTalkCarouselCommerceChannelSpecificMessageInternal,
)


ChannelSpecificMessageContentInternal = Union[
    FlowChannelSpecificMessageInternal,
    PaymentOrderDetailsChannelSpecificMessageInternal,
    PaymentOrderStatusChannelSpecificMessageInternal,
    KakaoTalkCommerceChannelSpecificMessageInternal,
    KakaoTalkCarouselCommerceChannelSpecificMessageInternal,
]
