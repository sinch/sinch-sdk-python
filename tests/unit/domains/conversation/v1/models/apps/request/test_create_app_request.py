import pytest
from pydantic import ValidationError

from sinch.core.exceptions import ValidationException
from sinch.domains.conversation.models.v1.apps.request.create_app_request import (
    CreateAppRequest,
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
    StaticBearerChannelCredentials,
    StaticTokenChannelCredentials,
)


def test_create_app_request_expects_parsed_input():
    """Test that the model correctly parses an input with all parameters set."""
    model = CreateAppRequest(
        channel_credentials={
            "SMS": {"token": "my-token", "claimed_identity": "identity"}
        },
        display_name="My App",
        conversation_metadata_report_view="FULL",
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
        event_destination_settings={
            "secret_for_overridden_callback_urls": "secret"
        },
        message_retry_settings={"retry_duration": 300},
        delivery_report_based_fallback={
            "enabled": True,
            "delivery_report_waiting_time": 60,
        },
    )

    assert len(model.channel_credentials) == 1
    assert isinstance(model.channel_credentials[0], StaticBearerChannelCredentials)
    assert model.channel_credentials[0].static_bearer.token == "my-token"
    assert model.channel_credentials[0].static_bearer.claimed_identity == "identity"
    assert model.channel_credentials[0].channel == "SMS"
    assert model.display_name == "My App"
    assert model.conversation_metadata_report_view == "FULL"
    assert isinstance(model.retention_policy, RetentionPolicy)
    assert model.retention_policy.retention_type == "MESSAGE_EXPIRE_POLICY"
    assert model.retention_policy.ttl_days == 180
    assert isinstance(model.dispatch_retention_policy, DispatchRetentionPolicy)
    assert model.dispatch_retention_policy.ttl_days == 7
    assert model.processing_mode == "CONVERSATION"
    assert isinstance(model.smart_conversation, SmartConversation)
    assert model.smart_conversation.enabled is True
    assert isinstance(model.event_destination_settings, EventDestinationSettings)
    assert model.event_destination_settings.secret_for_overridden_target == "secret"
    assert isinstance(model.message_retry_settings, MessageRetrySettings)
    assert model.message_retry_settings.retry_duration == 300
    assert isinstance(
        model.delivery_report_based_fallback, DeliveryReportBasedFallback
    )
    assert model.delivery_report_based_fallback.enabled is True
    assert model.delivery_report_based_fallback.delivery_report_waiting_time == 60

    # Asserting aliases on dump by alias
    alias_dump = model.model_dump(by_alias=True, exclude_none=True)
    assert "callback_settings" in alias_dump
    assert alias_dump["callback_settings"]["secret_for_overridden_callback_urls"] == "secret"


def test_create_app_request_raise_validation_exception_when_channel_credentials_is_a_list():
    """Test that a channel-keyed credentials map is normalized into the array form."""
    with pytest.raises(ValidationException) as excinfo:
        CreateAppRequest(
        channel_credentials=[],
        display_name="My App",
    )

    assert str(excinfo.value) == "channel_credentials must be a dict, not a list."
    assert excinfo.value.is_from_server == False

def test_create_app_request_expects_optionals_default_to_none():
    """Test that all optional fields default to None when only required fields are set."""
    model = CreateAppRequest(
        channel_credentials={
            "SMS": {"token": "my-token", "claimed_identity": "identity"}
        },
        display_name="My App",
    )

    assert model.conversation_metadata_report_view is None
    assert model.retention_policy is None
    assert model.dispatch_retention_policy is None
    assert model.processing_mode is None
    assert model.smart_conversation is None
    assert model.event_destination_settings is None
    assert model.message_retry_settings is None
    assert model.delivery_report_based_fallback is None


@pytest.mark.parametrize("missing", ["channel_credentials", "display_name"])
def test_create_app_request_expects_validation_error_for_missing_required(missing):
    """Test that a ValidationError is raised when a required field is missing."""
    data = {
        "channel_credentials": {
            "SMS": {"token": "my-token", "claimed_identity": "identity"}
        },
        "display_name": "My App",
    }
    del data[missing]

    with pytest.raises(ValidationError) as excinfo:
        CreateAppRequest(**data)

    assert missing in str(excinfo.value)

