from dataclasses import dataclass
from sinch.core.models.base_model import SinchRequestBaseModel


@dataclass
class ConversationRequest(SinchRequestBaseModel):
    app_id: str
    contact_id: str
    active: bool
    active_channel: str
    app_id: str
    contact_id: str
    metadata: str
    conversation_metadata: dict


@dataclass
class CreateConversationRequest(ConversationRequest):
    id: str


@dataclass
class ListConversationsRequest(SinchRequestBaseModel):
    app_id: str
    contact_id: str
    only_active: bool
    page_size: int
    page_token: str


@dataclass
class GetConversationRequest(SinchRequestBaseModel):
    conversation_id: str


@dataclass
class DeleteConversationRequest(SinchRequestBaseModel):
    conversation_id: str


@dataclass
class UpdateConversationRequest(ConversationRequest):
    update_mask: str
    metadata_update_strategy: str
    conversation_id: str


@dataclass
class StopConversationRequest(SinchRequestBaseModel):
    conversation_id: str


@dataclass
class InjectMessageToConversationRequest(SinchRequestBaseModel):
    conversation_id: str
    accept_time: str
    app_message: dict
    channel_identity: dict
    contact_id: str
    contact_message: dict
    direction: str
    metadata: str
