from typing import Annotated, Union

from pydantic import Field

from sinch.core.models.internal.unions import ResolveUnion
from sinch.domains.conversation.models.v1.sinch_events.inbound.payment_status_update_event import (
    PaymentStatusUpdateEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.inbound.reaction_event import (
    ReactionEvent,
)
from sinch.domains.conversation.models.v1.sinch_events.inbound.shortlink_activated_event import (
    ShortLinkActivatedEvent,
)
from sinch.domains.conversation.sinch_events.v1.internal import SinchEvent


class PaymentStatusUpdateContactMessageEvent(SinchEvent):
    payment_status_update_event: PaymentStatusUpdateEvent = Field(
        description="Message specific only for Payments feature to reflect current state of particular Payment Flow.",
    )


class ShortLinkActivatedContactMessageEvent(SinchEvent):
    shortlink_activated_event: ShortLinkActivatedEvent = Field(
        description="Object reflecting an event that is created when a contact visits a shortlink. Currently, this is only supported for the Messenger and Instagram channels.",
    )


class ReactionContactMessageEvent(SinchEvent):
    reaction_event: ReactionEvent = Field(
        description="Object reflecting an event that is created when a contact reacts/unreacts with an emoji to a particular MT message. Currently, this is only supported for the Messenger and Instagram channels.",
    )


ContactMessageEvent = Annotated[
    Union[
        PaymentStatusUpdateContactMessageEvent,
        ShortLinkActivatedContactMessageEvent,
        ReactionContactMessageEvent,
    ],
    ResolveUnion(),
]
