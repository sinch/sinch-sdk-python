from dataclasses import dataclass
from typing import Optional
from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class ListConversationMessagesRequest(SinchRequestBaseModel):
    conversation_id: Optional[str]
    contact_id: Optional[str]
    app_id: Optional[str]
    page_size: Optional[int]
    page_token: Optional[str]
    view: Optional[str]
    messages_source: Optional[str]
    only_recipient_originated: Optional[bool]


@dataclass
class GetConversationMessageRequest(SinchRequestBaseModel):
    message_id: str
    messages_source: str


@dataclass
class DeleteConversationMessageRequest(SinchRequestBaseModel):
    message_id: str
    messages_source: str


@dataclass
class SendConversationMessageRequest(SinchRequestBaseModel):
    app_id: str
    recipient: dict
    message: dict
    callback_url: str
    processing_strategy: Optional[str]
    channel_priority_order: list
    channel_properties: dict
    message_metadata: str
    conversation_metadata: dict
    queue: str
    ttl: str
    processing_strategy: str
