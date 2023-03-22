from dataclasses import dataclass
from typing import List, Optional
from sinch.core.models.base_model import SinchRequestBaseModel
from sinch.domains.conversation.models import (
    SinchConversationChannelIdentities,
    SinchConversationRecipient
)

from sinch.domains.conversation.enums import (
    ConversationChannel
)


@dataclass
class CreateConversationContactRequest(SinchRequestBaseModel):
    language: str
    channel_identities: Optional[List[SinchConversationChannelIdentities]]
    channel_priority: Optional[List[str]]
    display_name: Optional[str]
    email: Optional[str]
    external_id: Optional[str]
    metadata: Optional[str]


@dataclass
class UpdateConversationContactRequest(CreateConversationContactRequest):
    id: str


@dataclass
class ListConversationContactRequest(SinchRequestBaseModel):
    page_size: int
    page_token: str
    external_id: str
    channel: str
    identity: str


@dataclass
class DeleteConversationContactRequest(SinchRequestBaseModel):
    contact_id: str


@dataclass
class GetConversationContactRequest(SinchRequestBaseModel):
    contact_id: str


@dataclass
class MergeConversationContactsRequest(SinchRequestBaseModel):
    destination_id: str
    source_id: str
    strategy: str


@dataclass
class GetConversationChannelProfileRequest(SinchRequestBaseModel):
    app_id: str
    recipient: SinchConversationRecipient
    channel: ConversationChannel
