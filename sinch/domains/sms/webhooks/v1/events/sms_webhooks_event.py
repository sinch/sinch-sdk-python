from datetime import datetime
from typing import Optional, Union, Literal, Annotated
from pydantic import Field, StrictStr, StrictInt, conlist
from sinch.domains.sms.webhooks.v1.internal import WebhookEvent


class MediaItem(WebhookEvent):
    url: StrictStr = Field(..., description="URL to the media file")
    content_type: StrictStr = Field(
        ..., description="Content type of the media file"
    )
    status: Union[Literal["Uploaded", "Failed"], StrictStr] = Field(
        ..., description="Status of the media upload"
    )
    code: StrictInt = Field(..., description="Status code")


class MediaBody(WebhookEvent):
    subject: Optional[StrictStr] = Field(
        default=None, description="The subject text"
    )
    message: Optional[StrictStr] = Field(
        default=None, description="The message text"
    )
    media: conlist(MediaItem) = Field(..., description="Array of media items")


class BaseIncomingSMSWebhookEvent(WebhookEvent):
    from_: StrictStr = Field(
        ...,
        alias="from",
        description="The phone number that sent the message.",
    )
    id: StrictStr = Field(..., description="The ID of this inbound message.")
    received_at: datetime = Field(
        ...,
        description="When the system received the message. Formatted as ISO-8601: YYYY-MM-DDThh:mm:ss.SSSZ.",
    )
    to: StrictStr = Field(
        ...,
        description="The Sinch phone number or short code to which the message was sent.",
    )
    client_reference: Optional[StrictStr] = Field(
        default=None,
        description="If this inbound message is in response to a previously sent message that contained a client reference, then this field contains that client reference. Utilizing this feature requires additional setup on your account.",
    )
    operator_id: Optional[StrictStr] = Field(
        default=None,
        description="The MCC/MNC of the sender's operator if known.",
    )
    sent_at: Optional[datetime] = Field(
        default=None,
        description="When the message left the originating device. Only available if provided by operator. Formatted as ISO-8601: YYYY-MM-DDThh:mm:ss.SSSZ.",
    )


class MOTextWebhookEvent(BaseIncomingSMSWebhookEvent):
    body: StrictStr = Field(
        ...,
        description="The incoming message body. Maximum 2000 characters.",
    )
    type: Literal["mo_text"] = Field(
        ..., description="The type of incoming message. Regular SMS."
    )


class MOBinaryWebhookEvent(BaseIncomingSMSWebhookEvent):
    body: StrictStr = Field(
        ..., description="The incoming message body (Base64 encoded)."
    )
    type: Literal["mo_binary"] = Field(
        ..., description="The type of incoming message. Binary SMS."
    )
    udh: StrictStr = Field(
        ..., description="The UDH header of a binary message HEX encoded."
    )


class MOMediaWebhookEvent(BaseIncomingSMSWebhookEvent):
    body: MediaBody = Field(
        ...,
        description="The media message body containing subject, message, and media items.",
    )
    type: Literal["mo_media"] = Field(
        ..., description="The type of incoming message. MMS."
    )


# Union type for isinstance checks
_IncomingSMSWebhookEventUnion = Union[
    MOTextWebhookEvent, MOBinaryWebhookEvent, MOMediaWebhookEvent
]

# Discriminated union for validation
IncomingSMSWebhookEvent = Annotated[
    _IncomingSMSWebhookEventUnion, Field(discriminator="type")
]
