from typing import Annotated, Union
from sinch.core.models.internal.unions import ResolveUnion

from sinch.domains.conversation.models.v1.sinch_events.events.conversation_sinch_event_base import (
    ConversationSinchEventBase,
)
from sinch.domains.conversation.models.v1.sinch_events.events.message_delivery_receipt_event import (
    MessageDeliveryReceiptEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.events.message_inbound_event import (
    MessageInboundEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.events.message_submit_event import (
    MessageSubmitEvent,
)


ConversationSinchEventPayload = Annotated[
    Union[
        MessageDeliveryReceiptEvent,
        MessageInboundEvent,
        MessageSubmitEvent,
        ConversationSinchEventBase,
    ],
    ResolveUnion(fallback=ConversationSinchEventBase),
]
