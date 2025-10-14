from dataclasses import dataclass
from typing import Optional
from sinch.core.models.base_model import SinchRequestBaseModel
from sinch.domains.conversation.models import SinchConversationRetentionPolicy
from sinch.domains.conversation.enums import ConversationMetadataReportView, ConversationProcessingMode


@dataclass
class CreateConversationAppRequest(SinchRequestBaseModel):
    display_name: str
    channel_credentials: Optional[list]
    processing_mode: Optional[ConversationProcessingMode]
    conversation_metadata_report_view: Optional[ConversationMetadataReportView]
    retention_policy: Optional[SinchConversationRetentionPolicy]
    dispatch_retention_policy: Optional[SinchConversationRetentionPolicy]


@dataclass
class DeleteConversationAppRequest(SinchRequestBaseModel):
    app_id: str


@dataclass
class GetConversationAppRequest(SinchRequestBaseModel):
    app_id: str


@dataclass
class UpdateConversationAppRequest(CreateConversationAppRequest):
    app_id: str
    update_mask: list
