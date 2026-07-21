"""Unit tests for AppCustomResponse."""
import pytest
from pydantic import ValidationError

from sinch.domains.conversation.models.v1.apps.response.app_custom_response import (
    AppCustomResponse,
)
from sinch.domains.conversation.models.v1.credentials.shared.conversation_channel_credentials_response import (
    ConversationChannelCredentialsResponse,
    StaticBearerChannelCredentialsResponse,
)


def test_app_custom_response_expects_array_mapped_to_channel_map():
    """A raw server array is mapped to the channel-keyed response model."""
    model = AppCustomResponse.model_validate(
        {
            "id": "app-1",
            "display_name": "My App",
            "channel_credentials": [
                {
                    "channel": "SMS",
                    "static_bearer": {
                        "claimed_identity": "sp-id",
                        "token": "my-token",
                    },
                    "callback_secret": "secret",
                    "credential_ordinal_number": 2,
                    "state": {"status": "OK"},
                    "channel_known_id": "known-id",
                },
            ],
        }
    )

    assert isinstance(
        model.channel_credentials, ConversationChannelCredentialsResponse
    )
    credentials = model.channel_credentials

    assert isinstance(credentials.sms, StaticBearerChannelCredentialsResponse)
    assert credentials.sms.claimed_identity == "sp-id"
    assert credentials.sms.token == "my-token"
    assert credentials.sms.callback_secret == "secret"
    assert credentials.sms.credential_ordinal_number == 2
    assert credentials.sms.state.status == "OK"
    assert credentials.sms.channel_known_id == "known-id"


def test_app_custom_response_raises_validation_error_when_wrong_channel_credentials():
    """"""
    with pytest.raises(ValidationError):
        AppCustomResponse.model_validate(
            {
                "id": "app-1",
                "display_name": "My App",
                "channel_credentials": [
                    {"channel": "SMS", "static_token": {"token": "my-token"}}
                ],
            }
        )

