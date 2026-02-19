from datetime import datetime
from typing import Any, Optional, Union
from pydantic import Field, StrictStr

from sinch.domains.conversation.webhooks.v1.internal import WebhookEvent
from sinch.domains.conversation.models.v1.messages.shared import (
    ChannelIdentity,
    Reason,
)
from sinch.domains.conversation.models.v1.messages.shared.message_common_props import (
    MessageCommonProps,
)
from sinch.domains.conversation.models.v1.messages.response.types.contact_message import (
    ContactMessage,
)
from sinch.domains.conversation.models.v1.messages.types.processing_mode_type import (
    ProcessingModeType,
)


class ConversationWebhookEventBase(WebhookEvent):
    """Base fields present on every Conversation API webhook payload."""

    app_id: Optional[StrictStr] = Field(
        default=None,
        description="Id of the subscribed app.",
    )
    project_id: Optional[StrictStr] = Field(
        default=None,
        description="The project ID of the app which has subscribed for the callback.",
    )
    accepted_time: Optional[datetime] = Field(
        default=None,
        description="Timestamp when the channel callback was accepted by the Conversation API.",
    )
    event_time: Optional[datetime] = Field(
        default=None,
        description="Timestamp of the event as provided by the underlying channels.",
    )
    message_metadata: Optional[StrictStr] = Field(
        default=None,
        description="Context-dependent metadata.",
    )
    correlation_id: Optional[StrictStr] = Field(
        default=None,
        description="Value from correlation_id of the send message request.",
    )
    channel_metadata: Optional[Any] = Field(
        default=None,
        description="Additional metadata from the channel.",
    )


class MessageDeliveryReport(WebhookEvent):
    """Delivery report for an app message (MESSAGE_DELIVERY trigger)."""

    message_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the message.",
    )
    conversation_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the conversation.",
    )
    status: Optional[StrictStr] = Field(
        default=None,
        description="Delivery status (QUEUED_ON_CHANNEL, DELIVERED, READ, FAILED, SWITCHING_CHANNEL).",
    )
    channel_identity: Optional[ChannelIdentity] = Field(
        default=None,
        description="Channel identity of the recipient.",
    )
    contact_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the contact.",
    )
    metadata: Optional[StrictStr] = Field(
        default=None,
        description="Metadata associated with the message.",
    )
    processing_mode: Optional[ProcessingModeType] = Field(
        default=None,
        description="Processing mode (CONVERSATION or DISPATCH).",
    )
    reason: Optional[Reason] = Field(
        default=None,
        description="Reason when status is FAILED.",
    )


class MessageDeliveryReceiptEvent(ConversationWebhookEventBase):
    """Webhook event for MESSAGE_DELIVERY (delivery receipt for app messages)."""

    message_delivery_report: MessageDeliveryReport = Field(
        default=None,
        description="The delivery report payload.",
    )


class InboundMessage(MessageCommonProps, WebhookEvent):
    """Inbound message container (contact message + channel/contact info)."""

    contact_message: Optional[ContactMessage] = Field(
        default=None,
        description="The contact (inbound) message content.",
    )


class MessageInboundEvent(ConversationWebhookEventBase):
    """Webhook event for MESSAGE_INBOUND (inbound message from user)."""

    message: InboundMessage = Field(
        description="The inbound message payload.",
    )


class MessageSubmitNotification(WebhookEvent):
    """Notification that an app message was submitted (MESSAGE_SUBMIT trigger)."""

    message_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the app message.",
    )
    conversation_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the conversation. Empty if processing_mode is DISPATCH.",
    )
    channel_identity: Optional[ChannelIdentity] = Field(
        default=None,
        description="Channel identity of the recipient.",
    )
    contact_id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the contact. Empty if processing_mode is DISPATCH.",
    )
    submitted_message: Optional[Any] = Field(
        default=None,
        description="The submitted app message content (AppMessage).",
    )
    metadata: Optional[StrictStr] = Field(
        default=None,
        description="Metadata from message_metadata of the Send Message request.",
    )
    processing_mode: Optional[ProcessingModeType] = Field(
        default=None,
        description="Processing mode (CONVERSATION or DISPATCH).",
    )


class MessageSubmitEvent(ConversationWebhookEventBase):
    """Webhook event for MESSAGE_SUBMIT (message submission notification)."""

    message_submit_notification: MessageSubmitNotification = Field(
        description="The message submit notification payload.",
    )


ConversationWebhookEvent = Union[
    MessageDeliveryReceiptEvent,
    MessageInboundEvent,
    MessageSubmitEvent,
    ConversationWebhookEventBase,
]
