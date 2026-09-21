import pytest
from pydantic import ValidationError

from sinch.core.exceptions import ValidationException
from sinch.domains.conversation.models.v1.apps.request.update_app_request import (
    UpdateAppRequest,
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
from sinch.domains.conversation.models.v1.apps.shared.retention_policy import (
    RetentionPolicy,
)
from sinch.domains.conversation.models.v1.apps.shared.smart_conversation import (
    SmartConversation,
)
from sinch.domains.conversation.models.v1.credentials.shared.conversation_channel_credentials import (
    StaticTokenChannelCredentials,
)


def test_update_app_request_expects_parsed_input():
    """Test that the model correctly parses an input with all parameters set."""
    model = UpdateAppRequest(
        app_id="01FC66621XXXXX119Z8PMV1QPQ",
        channel_credentials={"MESSENGER": {"token": "my-token"}},
        display_name="Updated App",
        conversation_metadata_report_view="NONE",
        retention_policy={
            "retention_type": "CONVERSATION_EXPIRE_POLICY",
            "ttl_days": 90,
        },
        dispatch_retention_policy={
            "retention_type": "MESSAGE_EXPIRE_POLICY",
            "ttl_days": 3,
        },
        processing_mode="DISPATCH",
        smart_conversation={"enabled": False},
        event_destination_settings={
            "secret_for_overridden_callback_urls": "secret"
        },
        message_retry_settings={"retry_duration": 600},
        delivery_report_based_fallback={
            "enabled": False,
            "delivery_report_waiting_time": 30,
        },
    )

    assert model.app_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert len(model.channel_credentials) == 1
    assert isinstance(model.channel_credentials[0], StaticTokenChannelCredentials)
    assert model.channel_credentials[0].static_token.token == "my-token"
    assert model.channel_credentials[0].channel == "MESSENGER"
    assert model.display_name == "Updated App"
    assert model.conversation_metadata_report_view == "NONE"
    assert isinstance(model.retention_policy, RetentionPolicy)
    assert model.retention_policy.retention_type == "CONVERSATION_EXPIRE_POLICY"
    assert model.retention_policy.ttl_days == 90
    assert isinstance(model.dispatch_retention_policy, DispatchRetentionPolicy)
    assert model.dispatch_retention_policy.ttl_days == 3
    assert model.processing_mode == "DISPATCH"
    assert isinstance(model.smart_conversation, SmartConversation)
    assert model.smart_conversation.enabled is False
    assert isinstance(model.event_destination_settings, EventDestinationSettings)
    assert model.event_destination_settings.secret_for_overridden_target == "secret"
    assert isinstance(model.message_retry_settings, MessageRetrySettings)
    assert model.message_retry_settings.retry_duration == 600
    assert isinstance(
        model.delivery_report_based_fallback, DeliveryReportBasedFallback
    )
    assert model.delivery_report_based_fallback.enabled is False
    assert model.delivery_report_based_fallback.delivery_report_waiting_time == 30

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert "callback_settings" in alias_dump
    assert alias_dump["callback_settings"]["secret_for_overridden_callback_urls"] == "secret"


def test_update_app_request_raise_validation_exception_when_channel_credentials_is_a_list():
    """Test that a channel-keyed credentials map is normalized into the array form."""
    with pytest.raises(ValidationException) as excinfo:
        UpdateAppRequest(
            app_id="01FC66621XXXXX119Z8PMV1QPQ",
            channel_credentials=[],
        )

    assert str(excinfo.value) == "channel_credentials must be a dict, not a list."
    assert excinfo.value.is_from_server == False


def test_update_app_request_expects_only_app_id_required():
    """Test that app_id is the only required field, all others defaulting to None."""
    model = UpdateAppRequest(app_id="01FC66621XXXXX119Z8PMV1QPQ")

    assert model.app_id == "01FC66621XXXXX119Z8PMV1QPQ"
    assert model.channel_credentials is None
    assert model.display_name is None
    assert model.conversation_metadata_report_view is None
    assert model.retention_policy is None
    assert model.dispatch_retention_policy is None
    assert model.processing_mode is None
    assert model.smart_conversation is None
    assert model.event_destination_settings is None
    assert model.message_retry_settings is None
    assert model.delivery_report_based_fallback is None


def test_update_app_request_expects_validation_error_for_missing_app_id():
    """Test that a ValidationError is raised when the required app_id is missing."""
    with pytest.raises(ValidationError) as excinfo:
        UpdateAppRequest(display_name="Updated App")

    assert "app_id" in str(excinfo.value)


