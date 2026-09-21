import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.apps.response.app_response import (
    AppResponse,
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
from sinch.domains.conversation.models.v1.credentials.shared.conversation_channel_credentials import (
    StaticTokenChannelCredentials,
)


def test_app_response_expects_all_defaults_to_none():
    """Test that all optional fields default to None."""
    model = AppResponse()

    assert model.channel_credentials is None
    assert model.conversation_metadata_report_view is None
    assert model.display_name is None
    assert model.id is None
    assert model.rate_limits is None
    assert model.retention_policy is None
    assert model.dispatch_retention_policy is None
    assert model.processing_mode is None
    assert model.smart_conversation is None
    assert model.queue_stats is None
    assert model.event_destination_settings is None
    assert model.delivery_report_based_fallback is None
    assert model.message_retry_settings is None


def test_app_response_expects_valid_input():
    """Test that the model correctly parses a full valid input, including all nested models."""
    model = AppResponse(
        channel_credentials=[
            {"channel": "MESSENGER", "static_token": {"token": "my-token"}}
        ],
        conversation_metadata_report_view="FULL",
        display_name="My App",
        id="01FC66621XXXXX119Z8PMV1QPQ",
        rate_limits={"inbound": 25, "outbound": 25, "webhooks": 25},
        retention_policy={
            "retention_type": "MESSAGE_EXPIRE_POLICY",
            "ttl_days": 180,
        },
        dispatch_retention_policy={
            "retention_type": "MESSAGE_EXPIRE_POLICY",
            "ttl_days": 7,
        },
        processing_mode="CONVERSATION",
        smart_conversation={"enabled": True},
        queue_stats={"outbound_size": 10, "outbound_limit": 500000},
        callback_settings={"secret_for_overridden_callback_urls": "secret"},
        delivery_report_based_fallback={
            "enabled": True,
            "delivery_report_waiting_time": 60,
        },
        message_retry_settings={"retry_duration": 300},
    )

    assert isinstance(model.channel_credentials[0], StaticTokenChannelCredentials)
    assert model.channel_credentials[0].static_token.token == "my-token"
    assert model.conversation_metadata_report_view == "FULL"
    assert model.display_name == "My App"
    assert model.id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert isinstance(model.rate_limits, RateLimits)
    assert model.rate_limits.inbound == 25
    assert model.rate_limits.events == 25
    assert isinstance(model.retention_policy, RetentionPolicy)
    assert model.retention_policy.ttl_days == 180
    assert isinstance(model.dispatch_retention_policy, DispatchRetentionPolicy)
    assert model.dispatch_retention_policy.ttl_days == 7
    assert model.processing_mode == "CONVERSATION"
    assert isinstance(model.smart_conversation, SmartConversation)
    assert model.smart_conversation.enabled is True
    assert isinstance(model.queue_stats, QueueStats)
    assert model.queue_stats.outbound_size == 10
    assert model.queue_stats.outbound_limit == 500000
    assert isinstance(model.event_destination_settings, EventDestinationSettings)
    assert model.event_destination_settings.secret_for_overridden_target == "secret"
    assert isinstance(
        model.delivery_report_based_fallback, DeliveryReportBasedFallback
    )
    assert model.delivery_report_based_fallback.enabled is True
    assert isinstance(model.message_retry_settings, MessageRetrySettings)
    assert model.message_retry_settings.retry_duration == 300