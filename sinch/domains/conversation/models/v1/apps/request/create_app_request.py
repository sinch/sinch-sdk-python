from typing import Optional

from pydantic import Field, StrictStr

from sinch.domains.conversation.models.v1.apps.shared.delivery_report_based_fallback import (
    DeliveryReportBasedFallback,
)
from sinch.domains.conversation.models.v1.apps.shared.dispatch_retention_policy import (
    DispatchRetentionPolicy,
)
from sinch.domains.conversation.models.v1.apps.shared.event_destination_settings import (
    EventDestinationSettings,
)
from sinch.domains.conversation.models.v1.apps.shared.message_retry_settings import (
    MessageRetrySettings,
)
from sinch.domains.conversation.models.v1.apps.shared.retention_policy import (
    RetentionPolicy,
)
from sinch.domains.conversation.models.v1.apps.shared.smart_conversation import (
    SmartConversation,
)
from sinch.domains.conversation.models.v1.apps.types.conversation_metadata_report_view_type import (
    ConversationMetadataReportViewType,
)
from sinch.domains.conversation.models.v1.credentials.internal.conversation_channel_credentials_request_list import (
    ConversationChannelCredentialsRequestList,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)
from sinch.domains.conversation.models.v1.types.processing_mode_type import (
    ProcessingModeType,
)


class CreateAppRequest(BaseModelConfiguration):
    channel_credentials: ConversationChannelCredentialsRequestList = Field(
        default=...,
        description="Channel credentials, keyed by channel. The order of the entries defines the app channel priority.",
    )
    conversation_metadata_report_view: Optional[
        ConversationMetadataReportViewType
    ] = None
    display_name: StrictStr = Field(
        default=..., description="The display name for the app."
    )
    retention_policy: Optional[RetentionPolicy] = None
    dispatch_retention_policy: Optional[DispatchRetentionPolicy] = None
    processing_mode: Optional[ProcessingModeType] = None
    smart_conversation: Optional[SmartConversation] = None
    event_destination_settings: Optional[EventDestinationSettings] = Field(
        default=None, alias="callback_settings"
    )
    message_retry_settings: Optional[MessageRetrySettings] = None
    delivery_report_based_fallback: Optional[DeliveryReportBasedFallback] = (
        None
    )
