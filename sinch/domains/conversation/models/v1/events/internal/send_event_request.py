from typing import Optional

from pydantic import Field, StrictStr, conlist

from sinch.domains.conversation.models.v1.events.shared.app_event import (
    AppEvent,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.messages.internal.request.recipient import (
    Recipient,
)
from sinch.domains.conversation.models.v1.messages.types.message_queue_type import (
    MessageQueueType,
)
from sinch.domains.conversation.models.v1.types.conversation_channel_type import (
    ConversationChannelType,
)


class SendEventRequest(BaseModelConfiguration):
    app_id: StrictStr = Field(
        default=..., description="The ID of the app sending the event."
    )
    event_destination_target: Optional[StrictStr] = Field(
        default=None,
        alias="callback_url",
        description="Overwrites the default event destination target for delivery receipts for this event. The REST URL should be of the form: `http://host[:port]/path`",
    )
    channel_priority_order: Optional[conlist(ConversationChannelType)] = Field(
        default=None,
        description="Optional. A single element array that dictates on what channel should the Conversation API try to send the event. It overrides any default set on the contact. Providing more than one option has no effect.",
    )
    event: AppEvent = Field(default=..., description="The event to be sent.")
    event_metadata: Optional[StrictStr] = Field(
        default=None,
        description="Optional. Eventual metadata that should be associated to the event.",
    )
    queue: Optional[MessageQueueType] = None
    recipient: Recipient = Field(
        default=..., description="Identifies the recipient."
    )
