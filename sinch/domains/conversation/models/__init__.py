from dataclasses import dataclass
from typing import Optional

from sinch.core.models.base_model import SinchBaseModel
from sinch.domains.conversation.enums import (
    ConversationChannel,
    ConversationRetentionPolicyType
)


@dataclass
class SinchConversationRecipient(SinchBaseModel):
    contact_id: str


@dataclass
class SinchConversationTextMessage(SinchBaseModel):
    pass


@dataclass
class SinchConversationMessage(SinchBaseModel):
    id: str
    direction: str
    channel_identity: str
    app_message: dict
    conversation_id: str
    contact_id: str
    metadata: str
    accept_time: str
    sender_id: str
    processing_mode: str


@dataclass
class SinchConversationChannelIdentities(SinchBaseModel):
    channel: ConversationChannel
    identity: str
    app_id: str


@dataclass
class SinchConversationContact(SinchBaseModel):
    id: str
    channel_identities: SinchConversationChannelIdentities
    channel_priority: list
    display_name: str
    email: str
    external_id: str
    metadata: str
    language: str


@dataclass
class SinchConversationRetentionPolicy(SinchBaseModel):
    retention_type: ConversationRetentionPolicyType
    ttl_days: int


@dataclass
class SinchConversationTelegramCredentials(SinchBaseModel):  # TODO: add more communication channels
    token: str


@dataclass
class SinchConversationChannelCredentials(SinchBaseModel):
    channel: ConversationChannel
    callback_secret: Optional[str] = None
    telegram_credentials: Optional[SinchConversationTelegramCredentials] = None


@dataclass
class SinchConversationApp(SinchBaseModel):
    id: str
    channel_credentials: dict
    processing_mode: str
    conversation_metadata_report_view: str
    display_name: str
    rate_limits: dict
    retention_policy: dict
    dispatch_retention_policy: dict
    smart_conversation: dict
