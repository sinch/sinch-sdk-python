from typing import Optional
from pydantic import Field, StrictStr, conlist
from sinch.domains.conversation.models.v1.credentials.shared.conversation_channel_credentials import (
    ConversationChannelCredentials,
)
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
from sinch.domains.conversation.models.v1.apps.shared.queue_stats import (
    QueueStats,
)
from sinch.domains.conversation.models.v1.apps.shared.rate_limits import (
    RateLimits,
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
from sinch.domains.conversation.models.v1.types.processing_mode_type import (
    ProcessingModeType,
)
from sinch.domains.conversation.models.v1.internal.base.base_model_configuration import (
    BaseModelConfiguration,
)


class AppResponse(BaseModelConfiguration):
    channel_credentials: Optional[conlist(ConversationChannelCredentials)] = (
        None
    )
    conversation_metadata_report_view: Optional[
        ConversationMetadataReportViewType
    ] = None
    display_name: Optional[StrictStr] = Field(
        default=None, description="The display name for the app."
    )
    id: Optional[StrictStr] = Field(
        default=None,
        description="The ID of the app. You can find this on the [Sinch Dashboard](https://dashboard.sinch.com/convapi/apps).",
    )
    rate_limits: Optional[RateLimits] = None
    retention_policy: Optional[RetentionPolicy] = None
    dispatch_retention_policy: Optional[DispatchRetentionPolicy] = None
    processing_mode: Optional[ProcessingModeType] = None
    smart_conversation: Optional[SmartConversation] = None
    queue_stats: Optional[QueueStats] = None
    event_destination_settings: Optional[EventDestinationSettings] = Field(
        default=None, alias="callback_settings"
    )
    delivery_report_based_fallback: Optional[DeliveryReportBasedFallback] = (
        None
    )
    message_retry_settings: Optional[MessageRetrySettings] = None
